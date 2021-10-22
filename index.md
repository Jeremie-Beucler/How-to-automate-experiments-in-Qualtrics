# How to automate experiments in Qualtrics

This Github page explains how to partially automate experiments generation on Qualtrics using `Python`. Note that you may do the same thing using `R` or a similar programmation language.

This page would not have been created without Matthieu Raoelison, who came up with this process in the first place.

## Introduction

Qualtrics is an online software that allows to generate online surveys. However, some people use it to design scientific psychology experiments, for several reasons. For instance, it is [very easy](https://researcher-help.prolific.co/hc/en-gb/articles/360009224113-Qualtrics-Integration-Guide#heading-1) to run an online experiment using Qualtrics and the participants recruitment platform [Prolific](https://www.prolific.com/).

This (mis)use of Qualtrics can be quite problematic. Although you can insert some [Javascript code](https://www.qualtrics.com/support/survey-platform/survey-module/question-options/add-javascript/) in your questions and add some logic to your experiment using the [Survey flow](https://www.qualtrics.com/support/survey-platform/survey-module/survey-flow/survey-flow-overview/), Qualtrics still remains a "point and click" software.

Suppose you want to generate a psychology experiment in Qualtrics. In one trial, you may want to display a fixation cross for a given time, show a stimulus  and then record participants answers to this stimulus. In Qualtrics, generating this trial is quite easy.

However, your experiment may contain different conditions with several trials ... If you try to implement this on Qualtrics by hand, it will both take a lot of time and probably lead to errors. Even worse, suppose you painfully managed to build your experiment, and you realize you wanted the fixation cross to be displayed for only one second, and not two. You now have to modify each trial individually. Uh-oh ...  This is the kind of task where you may want to use programming !

## General overview

Here is a brief summary of the different steps for automating experiments in Qualtrics :

1. Prepare a list of your different items (e.g., in a `.csv` file);
2. Write a first program that generates the structure of your experiment using this list;
3. Save the result in a `.txt` file and import it on Qualtrics;
4. Fully customize one item on Qualtrics by hand;
5. Export your survey in a `.qsf` file;
6. Open this `.qsf` file on Python using a `json` decoder;
7. Copy the configuration of the manually customized item onto the other items;
8. Save the new `.qsf` file and import it on Qualtrics;
9. If you want to change something in your items configuration : *go back to step 4;*

You may have noticed that this is not a fully automated process. Indeed, steps 3, 4, 5 and 8 require to use Qualtrics, either to manually customize one item, or to import and export the survey at its different stages. However, these operations are very easy to perform and do not take a lot of time on the whole.

## STEP 1 : Prepare a list of your different items


