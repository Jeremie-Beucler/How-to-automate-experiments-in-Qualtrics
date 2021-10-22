# How to automate experiments in Qualtrics

This Github page explains how to partially automate experiments generation on Qualtrics using *Python*. Note that you may do the same thing using *R* or a similar programmation language.

I want to thank Matthieu Raoelison, who came up with this process

## Introduction

Qualtrics is an online software that allows to generate online surveys. However, some people use it to design scientific psychology experiments, for several reasons. For instance, it is [very easy](https://researcher-help.prolific.co/hc/en-gb/articles/360009224113-Qualtrics-Integration-Guide#heading-1) to run an online experiment using Qualtrics and the participants recruitment platform [Prolific](https://www.prolific.com/).

This (mis)use of Qualtrics can be quite problematic. Although you can add some [Javascript code](https://www.qualtrics.com/support/survey-platform/survey-module/question-options/add-javascript/) in your questions in Qualtrics, and add some logic to your experiment using the [Survey flow](https://www.qualtrics.com/support/survey-platform/survey-module/survey-flow/survey-flow-overview/), Qualtrics still remains a "point and click" software.

Suppose you want to generate a psychology experiment in Qualtrics. In one trial, you may for instance want to display a fixation cross for 1 second, show a stimulus for a certain time and then record the participant's answer and his confidence in the latter. In Qualtrics, generating this trial is quite an easy thing to do. However, your experiment may contain several trials, a counterbalancing, different conditions ... If you do this directly on Qualtrics, this will (1) take a lot of time and (2) probably lead to some mistakes being made (e.g., wrong naming of one item). These are generally two good reasons for using programmation !

## General overview of the 

We will start by briefly describing the 
