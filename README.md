# git-to-slack Hackathon Prototype

## Synopsis

A quick prototype that showcases the use of **Github** and **Slack** REST APIs.
The goal is to connect to a GitHub org using GitHub APIs, find all repositories with at least one open Pull Request,
and post the information on Slack using the Slack API.

## Installation

The main Python program is **git_to_slack.py**, all the rest of the files bieng the Python libraries explicitly added to the project directory in order to be packaged and executed as an **AWS Lambda**.

In order to install the function you just need to create a new AWS Lambda function and upload the prepared **git_to_slack.zip** ZIP file.

## Tests

The function expects an input parameter called **org** which specifies the Github org the function will scan for repositories to check. In our case we will test with the value **aws-quickstart**  

To thest the function we can either use the Test functionality of AWS Lambda, or trigger the Lambda function using AWS API Gateway.
