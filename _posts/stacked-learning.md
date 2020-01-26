title: Stacked Learning
subtitle: Stack!
description: This article is ...
image_link: http://placehold.it/500x500
date: 2018-08-28

<p style='text-align: center;'>
In this post we are going to learn what stacked learning is and how it differs from other ensemble methods. There will be a brief discussion about its strengths and weaknesses and in the end we will work on a simple Python implementation of both a stacked regressor and a stacked classifier.
</p>

## Model Construction

Stacking is part of a greater family of meta-algorithms called ensemble methods, where several models are combined into one predictive model. The algorithm is relatively straight forward and it involves none of the statistical or mathematical procedures found in other ensemble methods (e.g. bootstrap sampling, gradient descent). It can be used for regression or classification problems.

1. For each base learner, split the data and the target into k folds of equal size.
2. Try to predict the target in each fold by training only on data not in this fold.
3. Concatenate all these predictions to a single vector.
4. Stack these M vectors (referred to as meta-features) column-wise, resulting in a n x M matrix, where n is the number of observations and M is the number of base learners.
5. Fit a meta-learner using the meta-feature matrix and the actual target vector.
6. Predict by averaging over all k variations of a model prediction for each of the m base learners. Use the resulting M x 1 vector as an input for the meta-learner, which outputs the final prediction. For binary classification problems predictions can be pooled instead of averaged, which is equivalent to averaging and then rounding to the nearest integer.

image

What is described in Step 1 and 2 is known as cross validation. Using this instead of predicting the target using data that the base model has already seen will prevent the algorithm from favoring base models that overfit the data.


Well performing models produce highly correlated meta-features, since they all try to capture the same data shape (that of the target variable). This means that ordinary least squared regression is not appropriate in regression settings, since it produces parameter estimates with high variances, which makes them unreliable.

An easy way to combat this problem is to introduce a penalty term to the least squares equation, which pushes the parameter estimates towards zero, decreasing the variance while adding a small bias. Methods of this kind are called shrinkage methods or regularization methods and the one we will use is called ridge regression, which utilizes the L2-norm as a penalizer.

<p>
\[\hat{\beta} = \arg \min_\beta \|y - X \beta \|_2^2 + \lambda \| \beta \|_2^2  \]


where \(X\) is the feature matrix, \(y\) is the target vector and \(\lambda > 0\) controls the degree of regularization. Note that usually when using ridge regression standardizing the features is required, but since for a set of reasonable models the predictions are close to the target, we will skip standardization and assume that the features are approximately equally scaled.
</p>

## How does it stack up against other methods?

Among ensemble methods, bagging and boosting have been part of the data science toolbelt for a long time (e.g. in the form of random forests or grandient boosted trees). The underlying assumption of these models is that a set of weak learners can create a single strong learner. Stacking doesn’t quite fit into this category of ensemble methods, since here the underlying assumption is that a set of arbitrary base learners can create a learner that performs better than the best learner among those base learners. This makes the use case for stacking different to that of other ensemble methods. Since any base learner can be used, different types of well tuned arbitrarily complex models can be combined to shave off small amounts of the prediction error for all sorts of regression or classification problems. The caveat here is that in reality this improvement might be minimal but come at great computational cost, which, depending on the application, might not be justifyable.

## Computational Cost

<p>
In addition to the added computational cost that comes with fitting multiple models, the cross-validation process is what makes stacked learning incredibly slow compared to other ensemble methods. For algorithms with linear time complexity w.r.t. the number of observations, computation time is increased by a factor of \(k-1\), since \(k \left( \frac{k-1}{k} \cdot n \right) = (k - 1) \cdot n\) where \(k\) is the number of folds and \(n\) is the number of obervations. For algorithms with quadratic time complexity w.r.t. the number of observations, the increase is nearly the same. Here we have \(k \left( \frac{k-1}{k} \cdot n \right)^2 = \left(k - 1 - \frac{k - 1}{k} \right) \cdot n^2\). The construction of the meta features and fitting of the meta learner is relatively inexpensive compared to the previous step, since no cross-validation is required and the number of features here is only \(M\), where \(M\) is the number of base learners.
</p>


## Implementing Stacked Regression in Python

We will write the stacked regressor class in accordance with the scikit-learn API, meaning it will have a fit method and a predict method and we can specify some parameters upon intialization. The fit method will take a feature matrix, a target vector and a list of instances of regression models as input and output nothing.

To evaluate whether the stacked model actually outperforms all single models, we can write a helper class that compares the errors of the models according to some prespecified error function.

## Implementing Stacked Classification in Python

For this post we are only going to implement the algorithm for the binary classifcation problem, since for the multiclass problem each base model would have to produce more than one meta-feature, making things a bit more complicated.

Many scikit-learn classification algorithms have a method called predict_proba in addition to predict. This method outputs values in [0, 1] instead of {0, 1}, where 0.5 is total uncertainty. Assuming the meta-learner we are using has this method, we can easily this for our classifier. Using predict_proba instead of predict when constructing the meta-features can lead to a more accurate result as well.





