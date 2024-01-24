# Contours
A simple CLI tool to extract things like receipts from an image containing multiple receipts.
# Why
My phone of 5 years was broken and wouldn't turn on. I handle a lot of financial transactions in my family and I lost the ability to have an automated environment to store these receipts along with my phone.  

I relied on this tool for a month and it served me well until I got my new phone.  

# Usage:
*Requires Python 3.11 or above*

1. Clone this repo  

`HTTP`
```
git clone https://github.com/rfdzan/contours.git
```
`SSH`
```
git clone git@github.com:rfdzan/contours.git
```
2. Create a virtual environment (Recommended)  
```
cd contours/
python -m venv .
```
3. Install dependencies (there's only OpenCV)
```
pip install -r requirements.txt
```
# How to Use:  
## First time user:  
Run `app/main.py` once, and close it. 
This is to make sure you have all the directories in the project folder:
1. `collage/`
2. `extracted_images/`

Or you can just create it manually, up to you.

## Moving on  
1. Put your collage image in the `collage/` folder.
2. Run `app/main.py`, and type in the collage image filename. It doesn't have to be exact, just a string of words that the filename contains is fine.
3. Press `enter` and your chopped-up image is in `extracted_images/`

