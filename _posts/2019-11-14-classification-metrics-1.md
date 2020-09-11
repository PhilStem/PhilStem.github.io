---
layout: post
title: An Extensive Overview of Classification Metrics pt. I
---

In the next two posts we will take a look at the definition and interpretation of many of the classification metrics you might come across when evaluating your classification models. In the first part we will cover the metrics themselves and in the second part we will cover micro scores and macro scores in the context of multiclass classificaiton and how to interpret the ROC curve and how it connects to the AUC score.

I will assume that you are already familiar with the concept of a confusion matrix (the four values in bold in the image below). If you are, you will be able to follow everything covered in this post. All the evaluation metrics are just functions of the four values found in the confusion matrix.

<!-- <img src="img/wiki_table.jpg" class="img-fluid"> -->
![wiki-table](/img/wiki_table.jpg){:class="img-fluid"}

We are going to look at a lot of conceptually similar metrics with similar names so it is important to keep things structured. This cheat sheet is basically a copy of <a href="https://en.wikipedia.org/wiki/Precision_and_recall#Definition_(classification_context)">this</a> Wikipedia table without the funky colour choices. It includes all the metrics that will be covered in this post.
<!-- You can download the html table here. -->

A note on the confusion matrix: Sometimes you might see a version with the off-diagonal and/or diagnoal elements switched. That doesn’t really change anything though, one is just the transpose of the other. Just keep in mind to look at the axis labels when it comes to interpreting the values in the cells.

## Two Ways to Look at the Problem

<div class="row">
    <div class="col-md-6" style="padding-top: 30px;">
        <img src="/img/cm_box_right.jpg" class="img-fluid">
    </div>
    <div class="col-md-6" style="padding-top: 30px;">
        <img src="/img/cm_box_left.jpg" class="img-fluid">
    </div>
</div>

Only looking at the absolute number of correct classifications won’t give us any insights. We have to consider the misclassifications as well. There are two ways to look at this. Either we compare the True positive predictions to all actual positives (green in the left/first image) or we compare the true positive predictions to all positive predictions (green in the right/second image). If a classifier performs equally well on all classes, these values are the same. The same logic is applied to the negatives.

## Sensitivity and Specificity

<b>Sensitivity</b> corresponds the question "Out of all actual positives, how many were classified correctly?". For some problems, e.g. the classification of images of cats and dogs, "positive" just refers to the class we’re interested in when calculating the metrics. For two classes, if we switch what class we’re interested in, the only thing that changes is the orientation of the confusion matrix.

<b>Specificity</b> corresponds the question "Out of all actual negatives, how many were classified correctly?". Ideally, we would want both sensitivity  and specificity to be as high as possible. In some cases one of the two metrics is more important than the other. For example, we would prefer a normal email to be wrongly classified as spam over a spam email to be wrongly classified as a normal email, so in this case we value sensitivity over specificity.

<p>
We could also look at the false negative rate and the false positive rate, but that would provide no further insight, since \(\mathrm{TPR} = (1 - \mathrm{FNR}) \) and \(\mathrm{TNR} = (1 - \mathrm{FPR})\). However, the \( \mathrm{FPR} \) will be important when we discuss ROC curves in part 2.
</p>

## Precision and Recall

<b>Precision</b> corresponds the question "Out of all positive predictions, how many were classified correctly?" When compared to precision, sensitivity is usually referred to as <b>recall</b>. These two are often looked at together, especially for classifiers that output probabilities instead of binary values for their predictions. Here we can choose a decision threshold somewhere between 0 and 1. Oftentimes higher recall means lower precision.

To illustrate this, look at the two images from before and imagine how moving the horizontal decision treshold from top to bottom would change the light green trapezoid on the left (representing Recall) and the light green trapezoid on the right (representing Precision). This also shows that while Recall has to go from 0 to 1, precision doesn’t. Ideally, Precision is high at every recall value. This motivates the AUC metric, which we will discuss in part 2.


## Six more Metrics

<b>Accuracy</b> is the most intuitive metric when it comes to classification. It is defined as the number of correct classifications divided by the total number of classifications. While it’s easy to interpret, it also has its shortcomings.

If there are more actual positives than actual negatives, the accuracy will reflect the classifiers performance on positives stronger than on negatives. The <b>balanced accuracy</b> score doesn’t have that problem, since it is calculated with the proportions of successful predictions.

<p>
The <b>bookmaker informedness</b>, also known as Youden’s J statistic is similar to the balanced accuracy, in that they’re simple transformations of each other (\( \textrm{BI} = 2 \cdot \textrm{BACC} - 1 \)) but it has a different interpretation, namely that it represents by how much a classifier is better (in terms of sensitivity) than random guessing.
</p>

<b>Markedness</b> is similar to the bookmaker Informedness but instead of focusing on rates, it focuses on prediction values. It is used less often but since it also measures performance it makes sense to include it as well, even though it does not have such a nice interpretation.

The <b>F1 score</b> takes both recall and precision into account by calculating the harmonic mean of the two. The harmonic mean is used instead of the arithmetic mean, since precision and recall differ in their denominator but have the same numerator. Out of the six metrics in this section, it is the only one that doesn’t take all the values in the confusion matrix into account. The true negatives are left out, which is a weak point of this score.

<p>
<b>Matthew’s correlation coefficient</b> is a correlation coefficient between the actual and predicted classifications. When guessing randomly, its expected value is 0 and a perfect classifier would get a value of 1. It is insensitive to class imbalance and takes all values of the confusion matrix into account, which makes it a solid choice for almost all cases. It can also be calculated as \( \mathrm{MCC} = \sqrt{\textrm{BI} \cdot \textrm{MK}} \).
</p>