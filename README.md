Contention
==========

This is a quick application to trigger contention on an entity in Google Datastore via Google App Engine. It leverages a task queue framework to insert tasks that update properties on the same entity.

This is purposely an anti-pattern to expose contention. YOU SHOULD ABSOLUTELY NOT DESIGN YOUR CODE TO WORK THIS WAY. This example is purely to help users understand how transaction contention occurs as well as how Google handles the contention.


### Getting Started

We recommend that you create a virtual environment for your project as we do install dependencies that will isolate them from other projects.

Once you have your environment setup run `make install` to install our dependencies. The production based dependencies will be installed to a vendor directory in the project root so they can be deployed with the project.

#### Running Locally

Run `make run` to run the project locally. You can then run the process by visiting http://localhost:8080


### Deployment

Follow the standard Google App Engine directions for creating a Google Cloud Project and the setup process for a Google App Engine project. This should include installing the local cloud sdk and `gcloud` command line tool.

If those are configured you can then run: `gcloud app deploy` to deploy the code into your GCP project.
