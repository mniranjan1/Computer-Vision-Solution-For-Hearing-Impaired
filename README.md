# Computer-Vision-Solution-For-Hearing-Impaired
When friends and family can no longer understand a person due to hearing impairment, simple chores like ordering meals, discussing financial problems at the bank, explaining the illness at the hospital, or even talking to friends and family can seem onerous.

The deaf community is unable to perform tasks that the majority of the population takes for granted, and as a result of these difficulties, they are frequently placed in degrading situations. In most circumstances, access to expert interpretation services is not possible, leaving many deaf people with underemployment, social isolation, and public health issues.

The main objective of this project is to the handle those kind of issues mentioned above and predict the necessary hand signs such that person with hearing-impaired will easily communicate with people at ease.

# Demo


# Technical Apsects
- Python 3.7 and more
- Important Libraries: sklearn, pandas, numpy, cassandra, tensorflow-gpu, keras
- Front-end: HTML, CSS
- Back-end: Flask framework
- IDE and Tools: VScode, Google Colab  
- Database: Cassandra
- Deployment: Localhost

# What we did here
1. The first thing we did was, we created 34 gesture samples using OpenCV. For each gesture we captured 2000 images which were 256×256 pixels.All these images were grayscaled at first then it was thresholded and stroed in the gestures/folder.
2. Learned what a CNN is and how it works. Best resources were Tensorflow's official website and lots of reseacrh papers.
3. Created a CNN which look a lot similar to this MNIST classifying model using both Tensorflow and Keras. If you want to add more gestures you might need to add your own layers and also tweak some parameters, that you have to do on your own
4. Then used the model which was trained on a video stream using OpenCV , it capture real time video with following functions :
 - Transformation
 - Smoothing
 - Edge Detection
 - Segmentation
 - Thresholding
 - Contours Detection
5. For the implementation of whole code till now in web framework , so we used flask as the backend for the web app development.
6. We first connected the flask web app with cassandra such that the data of users can be stored such as email, password etc for user authentication like a normal website.
7. Then we loaded the model implemented different functions for creating a whole website so that user will feel much more interactive with the website
8. Finally, after running the server we can surf through website with successful register and login. Then we can use the webcam through **camera page** for prediciton of hand signs to text and speech and **Speech to Text** to convert the desired speech to text with necessary steps.
These are the overall and basic steps of what we did in this whole project development.

# Installing the requirements
Code is written in Python 3.7 and more. If you don't have python installed on your system, click here https://www.python.org/downloads/ to install.
- Create virtual environment. I would recommend installing anaconda, click here https://www.anaconda.com/ to install, then after installation type command - conda create-n myenv python=3.7
- Activate the environment - conda activate myenv
- Install the required packages - pip install -r requirements.txt

# How to use this Repo
Before using this repo, let me tell about something if you are true lover of machine learning and want to use this repo for research purpose and more willing to flourish your skill in machine learning then you have to follow each steps from the beginning of creating dataset to the deployment but If you want to just try to use the website of flask then refer to Basic use of this Repo below:

**Full steps for using this Repo**
**1. Creating a gesture**
 - First set suitable parameters of the images, location of storing images
 - Then run the following command :
 
```` 
python 1_img_cap.py
````
 - AFter that, you have to type gesture no, and gesture name/text
 - Then two window will appear at first "Video Feed 1" and "Video Feed" for gray and normal video respectively
 - You can press "c" letter on for start capturing images when youre ready
 - "Capturing..." will be shown along with a threshold window
 - Finally after completetion the window will automatically close 
 - If you want to add another gesture then rerun the program and repeat above steps  

**2. Creating dataset**
- First run the following command  and make sure that gestures folder is in the same path
````
python 2_create_dataset.py
````
- Then it will automatically locate those images and create the dataset by help of pickle dumping those images in pickle readable format.
I Would suggest using Google colab for creating dataset as it requires more RAM according to the size and number of images.


 
