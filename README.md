---
date: 2024-04-12T15:17:12.815702
author: AutoGPT <info@agpt.co>
---

# image maker

Based on the information gathered from our discussion and searches, the goal is to create images from input text leveraging some of the most advanced tools available. The user has a preference for images generated in a specific style or theme and intends to use these images across various applications, possibly including branding, personal projects, advertisements, or entertainment. From the research conducted, the best tools for generating images from text include DALL·E 2 by OpenAI, Artbreeder, DeepArt, and Runway ML. These tools utilize cutting-edge AI algorithms to transform textual descriptions into visual images that meet a wide array of needs, aligning well with the user's requirements. To embark on this project, the recommended approach would involve selecting one or more of these mentioned platforms based on the specific style, theme, and application requirements of the user, ensuring the generated images align perfectly with the user's vision and purpose.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'image maker'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
