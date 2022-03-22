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

# What I did here
1. The first thing i did was, I created 34 gesture samples using OpenCV. For each gesture I captured 2000 images which were 256 256 pixels.All these images were grayscaled at first then it was thresholded and stroed in the gestures/folder.
2. Learned what a CNN is and how it works. Best resources were Tensorflow's official website and lots of reseacrh papers.
3. Created a CNN which look a lot similar to this MNIST classifying model using both Tensorflow and Keras. If you want to add more gestures you might need to add your own layers and also tweak some parameters, that you have to do on your own
4. 

# Installing the requirements
Code is written in Python 3.7 and more. If you don't have python installed on your system, click here https://www.python.org/downloads/ to install.
- Create virtual environment. I would recommend installing anaconda, click here https://www.anaconda.com/ to install, then after installation type command - conda create-n myenv python=3.7
- Activate the environment - conda activate myenv
- Install the required packages - pip install -r requirements.txt
 
