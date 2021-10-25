# How to automate experiments in Qualtrics

This Github page explains how to partially automate experiments generation on Qualtrics using `Python`. Note that you may do the same thing using `R` or a similar programmation language.

This page would not have been created without Matthieu Raoelison, who came up with this process in the first place.

## Introduction

Qualtrics is an online software that allows to generate online surveys. However, some people use it to design scientific psychology experiments, for several reasons. For instance, it is [very easy](https://researcher-help.prolific.co/hc/en-gb/articles/360009224113-Qualtrics-Integration-Guide#heading-1) to run an online experiment using Qualtrics and the participants recruitment platform [Prolific](https://www.prolific.com/).

This (mis)use of Qualtrics can be quite problematic. Although you can insert some [Javascript code](https://www.qualtrics.com/support/survey-platform/survey-module/question-options/add-javascript/) in your questions and add some logic to your experiment using the [Survey flow](https://www.qualtrics.com/support/survey-platform/survey-module/survey-flow/survey-flow-overview/), Qualtrics still remains a "point and click" software.

Suppose you want to generate a psychology experiment in Qualtrics. In one trial, you may want to display a fixation cross for a given time, show a stimulus  and then record participants answers to this stimulus. In Qualtrics, generating this trial once is quite easy.

However, your experiment may contain different conditions, each one containing several trials ... If you try to implement this on Qualtrics by hand, it will take a lot of time and may lead to errors. Even worse, suppose you painfully managed to build your experiment, and you realize you wanted the fixation cross to be displayed not for two seconds, but only for one. You now have to modify each trial individually. Uh oh ...  This is the kind of task where you may want to use programming !

## General overview

Here is a brief summary of the different steps for automating experiments in Qualtrics :

1. Prepare a list of your different items (e.g., in a `.csv` file);
2. Write a program generating a `.txt` file with the complete structure of the experiment and import it on Qualtrics;
3. Fully customize one item on Qualtrics by hand;
4. Export your survey in a `.qsf` file and open this file on Python using a `json` decoder;
5. Copy the configuration of the manually customized item onto the other items and import the new `.qsf` file on Qualtrics;
6. If you want to change something in your items configuration : *go back to step 2;*

You may have noticed that this is not a fully automated process. You indeed have to manually customize one item on Qualtrics, or to import and export the survey at its different stages. However, these operations are very easy to perform and do not take a lot of time on the whole.

images :
- vue csv R id questions réponses
- .txt structure mcq
- vue csv x .txt structure = struct remplie
- txt flèche sur qualtrics
- vue qualtrics customize
- qualtrics => qsf file
- python / vue arbre qsf
- carré rouge sélection item => autre item
- qsf => qualtrics


## STEP 1 : Prepare a list of your different items

![csv_image](/images/csv_image.png)

Create a `.csv` file (or any format you find suitable, as long as you can read it on Python afterwards) containing what is gonna change from trial to trial : questions, possible answers ...

**Important** : you should also have a column containing the trial/item ID, in a structured way. This will be necessary to find your item in the `.qsf` file.

*Example : if you have two conditions - Conflict and No-Conflict - with 20 items in each, you can name your items : C_1, NC_1, C_2 ...*

## STEP 2 : Write a program generating a `.txt` file with the complete structure of the experiment and import it on Qualtrics;

Fortunately, Qualtrics allows you to import a simple survey structure in a `.txt` file, using a specific syntax.

Before proceeding, read the *Preparing a Simple Format TXT or DOC File* and the *Preparing an Advanced Format TXT or DOC File* sections of the following page, which explain the rules you have to follow in your `.txt` file : [How to import a survey on Qualtrics](https://www.qualtrics.com/support/survey-platform/survey-module/survey-tools/import-and-export-surveys/).




