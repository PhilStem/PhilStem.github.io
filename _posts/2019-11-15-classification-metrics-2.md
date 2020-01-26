---
layout: post
title: An Extensive Overview of Classification Metrics pt. II
---

In the last post we looked at the definitions and interpretations of various classificaiton metrics for the binary classificaiton problem. In this post we will extend those metrics to the multiclass classification problem. After that we will look at the ROC curve and the precision and recall curve and how prediction probabilites can be misleading.

## Micro and Macro Scores

<p>
In the multiclass classificaiton problem we have to make a decision on how to treat the \(C \times C \) confusion matrix where \( C > 2 \) such that the standard metrics can be applied. To calculate the <b>micro score</b>, the total number of true positives, false negatives and false positives are summed up for every class, resulting in \(C\) (one vs. all) \( 2 \times 2 \) confusion matrices which are summed up to a single confusion matrix from which the metric of interest is calcualted.</p>

<p>For the <b> macro score</b> the process is similar, only that \( C \) metrics of interest are calculated separately from the \(C\) (one vs. all) \( 2 \times 2 \) confusion matrices and then averaged. If classes are imbalanced, the <b>weighted macro score</b> gives more accuarte results, since instead of an unweighted mean metrics are weighted according to their class size.</p>

<div class="row">
    <div class="col-md-6" style="padding-top: 30px;">
        <img src="/img/micro.jpg" class="img-fluid">
    </div>
    <div class="col-md-6" style="padding-top: 30px; padding-bottom: 30px;">
        <img src="/img/macro.jpg" class="img-fluid">
    </div>
</div>

## Curves

In part 1 I already mentioned that some classification algorithms (logistic regression, neural networks, etc.) output probabilities instead of binary values which allows for an additional level of analysis. While we could just put the decision threshold at 0.5 and be done with it, there is some value in looking at a whole set of thresholds. Scanning through a list of equidistant values between 0 and 1 and recording two metrics at each threshold allows us to plot a curve on a cartesian coordinate systems.

Theoretically we could plot any metric against any other metric. In practice only two plots are used. Plotting the false positive rate (1 - Specificity) against the true positive rate (Sensitivity) results in the <b>ROC curve</b>. Let’s look at some images again to gain an intuitive understanding how it functions.

<div class="row">
    <div class="col-md-6" style="padding-top: 30px;">
        <img src="/img/cm_box_right.jpg" class="img-fluid">
    </div>
    <div class="col-md-6" style="padding-top: 30px;">
        <img src="/img/cm_box_curve.jpg" class="img-fluid">
    </div>
</div>

Moving the horizontal decision treshold from top to bottom would increase the false positive rate (dark blue part of blue triangle) but also increase the true positive rate (light green part of green triangle). On the left side, both values change by the same amount, which means that this classifier is exactly as good as random guessing. On the right side, as we move the decision threshold downwards from the top, the false positive rate increases by a little but the true positive rate increases by a lot. This means this classifier is better than the one on the left.

<div class="row">
    <div class="col-md-6" style="padding-top: 30px;">
        <img src="/img/AUC_left.jpg" class="img-fluid">
    </div>
    <div class="col-md-6" style="padding-top: 30px;">
        <img src="/img/AUC_right.jpg" class="img-fluid">
    </div>
</div>

If we now plot this moving of the decision threshold, we can see that the two classifiers’ graphs differ in size. This is the motivation behind the AUC (Area under the Curve) metric. In a multiclass setting we can use the one vs. all approach again for each class and just take the average of the AUC’s to calcuate an overall AUC.

<p>
The <b>precision-recall curve</b> works in a similar way, except that here, as the name suggests, we plot precision against recall. It is more useful when working with imbalanced classes but doesn’t take the true negative rate into account, so when classes are balanced, the ROC curve is preferred. The corresponding metric for this curve is the Average Precision score (AP), which can be defined as the sum of changes in recall at all thresholds \( n \) weighted by their respective precisions, which translates to the formula \( \mathrm{AP} = \sum_n (\mathrm{TPR}_n - \mathrm{TPR}_{n-1}) \mathrm{PPV}_n \).
</p>

## A caveat with prediction probabilities

One thing to watch out for with prediction probabilities is that the level of certainty with which a classifier predicts might not reflect its actual prediction capabilities. If a classifier outputs probabilities above 99% for all obvervations but in reality only 20% are correct, that might be misleading. This is why it's always a good idea to look at a <b>calibration plot</b>, in which probabilities are split into equally spaced bins and the fraction of positives in each bin is counted. A perfectly honest classifier would show a straight line from 0 to 1.

This honesty can be quantified with the <b>brier score</b>. It can be defined as the mean square error of predicted probabilities compared to actual outcomes and is low for honest models and high for dishonest models. Dishonest classifiers can be calibrated, either with sigmoid calibration or isotonic regression.

## Conclusion

<p>
If you look at this <a href="https://scikit-learn.org/stable/modules/model_evaluation.html#classification-metrics">scikit-learn page</a> for classification metrics you can see that there are still some metrics that we didn't cover. The ones we did cover have detailed explanations so why did I even bother writing two posts on this topic?
<!-- If you've ever studies linear models you've probably heard of the \( R^2 \) value. It represents the variation in the data explained by the models as a fraction of the total variation. Can you calculate it for a random forest model? Sure! Does it have the same interpretation? No. The assumptions for this to be true are not met. In the same sense, -->
I think it is helpful to understand the motivation behind every classification metric you use since not every metric is meaningful in every situation. What I'm gonna leave you with is <a href="https://youtu.be/nG3tT31nPmQ?t=6032">this video</a> by Jeremy Howard, in which he explains a method for image segmentation, specifically the section where he talks about accuracy scores.
</p>

<!-- ## Implementation in Python -->

<!-- The scikit-learn machine learning package provides many of the metrics mentioned in these posts. Still, I have decided to implement them myself in a very simple way so if you want to experiment yourself you don’t have to write them from scratch or sift through the scikit-learn files. You can get the python code here.

Finally, let’s try to evaulate a few classifiers with the metrics we have learned about. As a dataset i will use … . The classifiers I chose are the scikit-learn implementations of Random Forest, Logistic Regression and Naive Bayes. I won’t tune any hyperparameters or perform much preprocessing on the data, since that seems like overkill for this example. -->
