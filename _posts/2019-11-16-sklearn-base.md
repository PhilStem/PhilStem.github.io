---
layout: post
title: Writing an Estimator according to scikit-learn's Guidelines
---

Every regression, classification, clustering or transformation method provided by the scikit-learn package follows a strict standard of rules. This helps maximize consistency and ensures that methods incorporating these types of models (e.g. grid search, pipelining) work consistently. The scikit-learn documentation provides extensive [instructions](https://scikit-learn.org/stable/developers/contributing.html) on how to write code in such a way that users can expect the same interface from user contributed code as from library code. [The scikit-learn-contrib](https://github.com/scikit-learn-contrib) project is a collection of such projects, among them popular algorithms that didn't meet the inclusion criteria (e.g. the HDBSCAN clustering algorithm). In this post we'll look at what it means for code to be compliant with scikit-learn's standard, some tools to help with this and why this might be an interesting topic even for non-contributers.

## A Basic Estimator Class

Consider this simple task: Write a basic multiple linear regression (OLS) estimator in the style of scikit-learn! If you have a basic understanding of scikit-learn's interface, object oriented programming in python and statistics, the code you would come up with would probably look similar to this.

{% highlight python linenos %}
{% include_relative some_code.py %}
{% endhighlight %}

Would you say this is compliant with scikit-learn's standard? On the surface it seems so. This class has a constructor that takes the estimator's parameters, a fit method and a predict method.
Luckily `sklearn.utils.estimator_checks` provides the `check_estimator` function, which runs an extensive test-suite either on a class or an instance of class, to check if it adheres to scikit-learn conventions. Let's run it on our class and see what happens.

{% highlight python linenos %}
{% include_relative some_other_code.py %}
{% endhighlight %}

The `check_parameters_default_constructible` function called in the `check_estimator` funciton throws an error:

```
TypeError: Cannot clone object '<__main__.LinearRegressor object at 0x1a1deb2c18>' (type <class '__main__.LinearRegressor'>): it does not seem to be a scikit-learn estimator as it does not implement a 'get_params' methods.
```

We didn't implement a `get_params` method, which seems to be reqiured when using the `clone` function in `sklearn.base`. Luckily, since this method works the same for every estimator, sci-kit learn provides a base class from which this method can be inherited so we don't have to implement it ourselves.

## The `BaseEstimator` and `RegressorMixin` Classes

Let's take a closer look at the `sklearn.base` file, which contains the building blocks for scikit-learn's estimators. The first useful class is the `BaseEstimator` class. Every estimator is a subclass of the `BaseEstimator` class. It provides two public methods: `get_params` and `set_params`. Having these methods is not only useful as an alternative way to input parameters but also necessary when using scikit-learn's grid search interface or when cloning an estimator.

The second useful class for our case is the `RegressorMixin` class. The concept of a [mixin](https://en.wikipedia.org/wiki/Mixin) is not exclusive to scikit-learn or python but comes from OOP and is defined as a class that contains methods for use by other classes without having to be the parent class of those other classes. Scikit-learn's mixins provide little functionality. All mixins set the attribute `_estimator_type`, which is important when using [cross validation](https://scikit-learn.org/stable/developers/contributing.html#estimator-types). The `RegressorMixin` and `ClassifierMixin` classes also provide a default scoring method, which implements the R2 score and the accuracy score respectively.

Let's try to run `check_estimator` again, but this time with the following modification to the head of our file:

{% highlight python linenos %}
import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin

class LinearRegressor(BaseEstimator, RegressorMixin):
...
{% endhighlight %}

This time the `lstsq` function throws an error:

```
TypeError: No loop matching the specified signature and casting was found for ufunc lstsq_n
```

This error is caused by the `check_dtype_object` function called in `check_estimator`. To understand the reason why, we first have to look at how numpy handles a specific data type.

## Data Types in numpy

In addition to testing the fit and predict methods with input of data types `np.int32`, `np.int64`, `np.float32` and `np.float64`, `check_estimator` also calls the function `check_dtype_object`, which tests if the fit and predict methods fail for inputs of data type `object`, which is a build-int python data type. An array with this type is different from a normal numpy array. It is not filled with objects of type `int` or `float` but with pointers to objects. These objects are not stored in a contiguous block of memory and thus can have different sizes. The following code is therefore valid.

{% highlight python linenos %}
object_array = np.array([1.0, 'foo', 3.0], dtype=object)
doubled_object_array = 2 * object_array
{% endhighlight %}

scikit-learn accepts numpy arrays of type `object`, but the `lstsq` function doesn't know how to deal with them, which results in an error. Our estimator should therefore cast numpy arrays of type `objects` into a type the `lstsq` function can deal with. Again, we don't have to implement this functionality ourselves, since `sklearn.utils.validation` already includes the `check_X_y`  and `check_array` functions that can help us with that.


## Validation Utilities

In addition to the two aforementioned functions we can also use the `check_is_fitted` function from the same file to see if the fit method has been called on an instance of our estimator class. Now we can prepend our class methods with the following lines and see if our class passes the test. (For now we will keep it simple and not accept sparse matrix representations.)

{% highlight python linenos %}
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
...

    def fit(self, X, y):
        X, y = check_X_y(X, y, accept_sparse=False, y_numeric=True)
        self.is_fitted_ = True
        ...

    def predict(self, X):
        X = check_array(X, accept_sparse=False)
        check_is_fitted(self, 'is_fitted_')
        ...
{% endhighlight %}

The program now terminates without errors. The `check_array` function (which is also called inside the `check_X_y` function) saved us, since it not only throws an error if a certain specified condition on the input is not met but also converts an array of type `object` to type `np.float64` if possible.

## Conculsion

The actual implementation of linear regression in scikit-learn accepts sparse matrices, multidimensional targets and has a lot more functionality. That's all nice to have but the most important feature is that the code works for the data it should work for and throws appropriate errors for the data it should not work for. This also applies to our simple class and even though I didn't check every error `check_estimator` can throw, I trust scikit-learn's validation utilities to take care of that and if time is not an issue I could use them as a foundation to write my own. Even if perfect compliance is not the goal, these utilities could save you a lot of time and frustration. You can find the full python code for the class we've written with added docstrings here.
