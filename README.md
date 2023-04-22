# ForkMyLife


**ForkMyLife: turning boring READMEs into stunning web pages, so you can finally impress your developer crush.**

ForkMyLife is a command-line utility built in Python that allows you to fork any public public repository and convert its README.md file to HTML, add some CSS, and deploy it to Vercel. ForkMyLife supports supports GitHub, Bitbucket, FriendCode, Assembla ...

# Requirements

  * Python 3.6 or higher
  * Git
  * Vercel account and API token

# Installation

1. Clone the repository:

   `git clone https://github.com/hitbug-exe/ForkMyLife.git`

2. Install the required packages using pip:

   `pip install -r requirements.txt`

3. Install the vercel CLI:

   `nmp i -g vercel`

# Usage

To use ForkMyLife, simply run the command:

  `ForkMyLife <git url> <vercel token>`

Replace <git url> with the URL of the public repository you want to fork, and <vercel token> with your Vercel API token.

For example:

  `ForkMyLife git@bitbucket.org:/ForkMyLife.git abcdefghijklmnopqrstuvwxyz0123456789`

This will fork the hitbug-exe/ForkMyLife repository, convert its README.md file to HTML, add some CSS, and deploy it to Vercel using your API token.

# License

This project is licensed under the MIT License. Feel free to use, modify, and distribute it as you see fit.
