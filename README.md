# Computer-Vision-Solution-For-Hearing-Impaired
When friends and family can no longer understand a person due to hearing impairment, simple chores like ordering meals, discussing financial problems at the bank, explaining the illness at the hospital, or even talking to friends and family can seem onerous.

The deaf community is unable to perform tasks that the majority of the population takes for granted, and as a result of these difficulties, they are frequently placed in degrading situations. In most circumstances, access to expert interpretation services is not possible, leaving many deaf people with underemployment, social isolation, and public health issues.

The main objective of this project is to the handle those kind of issues mentioned above and predict the necessary hand signs such that person with hearing-impaired will easily communicate with people at ease.

# Demo

https://user-images.githubusercontent.com/40750462/159876005-85d4a6e4-ebd4-445b-9f6a-3fd52cf91a6e.mp4

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
I Would suggest using Google colab for creating dataset as it requires more RAM according to increase in size and number of images.
- It will create files for training and testing.

**3. Training Model**
- Run the following command and make sure that the train and test datasets are on same folder.
````
python 3_cnn_keras.py 

````
- Then it will start training . The time taken depends on the number of epochs and size of dataset as well.
- AFter completion of training phase the script will save the model in handsign.h5 file.

**4. Get Model Reports**
-To get the classification reports about the model make sure you have test_images and test_labels file which are generated by load_images.py. In case you do not have them run 2_create_dataset.py file again. Then run this file
````
python 5_get_model_reports
````
-You will get the confusion matrix, f scores, precision and recall for the predictions by the model.

**5. Displaying all gestures**
-To see all the gestures that are stored in 'gestures/' folder run this command
````
python 6_display_all_gestures.py
````
**6. Testing gestures**
We have created a python file which loads model and use OpenCV to create windows for opening webcam and test the trained hand signs thorugh real-time video interaction. It opens window just like in the step of capturing images and follows the same techniques of openCV.
 - First run the command
 ````
 python 4_cam_cnn_out.py
 ````
 - Wait for the overall process to load then similarly two types of window will open one is called Camera_Interface and other is Thresholded.
 - Keep your hand on the ROI with making desired hand signs such that the application can detect those signs in text and speech.
 
 Note: Wear glove and the background should be a wall or with less objects for increasing accuracy
 - You can hear the voice after succesfully predicting the letters and you can combine those letters to words and to sentence and in the end whole word or sentence can be heard in a form of speech 

**7. Running the Flask Application**
We have integrated everything the code of testing gesture python file to app.py such that it can run our desired outcome in flask web framework succesfully.
- Run the command
````
python wsgi.py
````
- Then server will load with necessary libraries and requirements
- Then click on the local host IP address
- Website will be opened and simply register and login as like we do in normal website
- Then after successful login you can checkout Camera page where you can predict the handsigns to text and speech.
- And you can also access Speech To Text page where audio can be converted to Text and the steps are simply mentioned in that web page as well.

We tried to deploy in the cloud related platforms but this project needed lots of requirements and for this we needed to use paid version of cloud which was not possible for us and similarly we had problem loading the camera in some cloud platforms. Therefore this project can be simply run in local host . But in near future if we tackled those difficulties then it will be surely deployed in various cloud platforms.

**Basic Steps :**
- Download the dataset and start from step 2 with given link https://www.kaggle.com/datasets/niranjanshrestha/gesturo

OR
- Download already trained model from this given link https://drive.google.com/file/d/1ktTOydOQHvEozrK2czrSb24eby_6GNHF/view?usp=sharing and start from step 4

# Project Documents
- HLD: https://github.com/mniranjan1/Computer-Vision-Solution-For-Hearing-Impaired/blob/master/DOCS/HLD.pdf 
- LLD: https://github.com/mniranjan1/Computer-Vision-Solution-For-Hearing-Impaired/blob/master/DOCS/LLD.pdf
- Architecture: https://github.com/mniranjan1/Computer-Vision-Solution-For-Hearing-Impaired/blob/master/DOCS/Architecture.pdf
- Wireframe: https://github.com/mniranjan1/Computer-Vision-Solution-For-Hearing-Impaired/blob/master/DOCS/Wireframe.pdf
- Detailed Project Report: https://github.com/mniranjan1/Computer-Vision-Solution-For-Hearing-Impaired/blob/master/DOCS/DPR.pdf



# Author
Niranjan Shrestha: https://www.linkedin.com/in/niranjan-shrestha/ 

Prajin Bajracharya: https://www.linkedin.com/in/prajinbajracharya/

# Got a question?
If you have any questions that are bothering you please contact me on my linkedin profile. Just do not ask me questions like where do I live, who do I work for etc. Also no questions like what does this line do. If you think a line is redundant or can be removed to make the program better then you can obviously ask me or make a pull request.

# Citation
[1] T.H. Samiha (TP034305) “Hand gesture recognition system” https://www.slideshare.net/AfnanRehman/hand-gesture-recognition-systemfyp-report-50225618 Internet:, July. 18, 2017 [Aug. 13, 2019].

[2]	Sign Language Spotting with a Threshold Model Based on Conditional Random Fields Hee-Deok Yang, Member, IEEE, Stan Sclaroff, Senior Member, IEEE, and Seong-Whan Lee, Senior Member, IEEE

[3]	SIGN LANGUAGE DETECTION USING 3D VISUAL CUES J.F. Lichtenauer G.A. ten Holt E.A. Hendriks M.J.T. Reinders Information and Communication Theory Group Faculty of Electrical Engineering, Mathematics and Computer Science (EEMCS) Delft University of Technology, The Netherlands

[4]	J. Davis and M. Shah et.al Visual Gesture Recognition

[5]	Shape-Based Hand Recognition by Erdem Yörük, Ender Konuko˘glu, Bülent Sankur, Senior Member, IEEE, and Jérôme Darbon

[6]	Recent developments in visual sign language recognition by Ulrich von Agris Æ Jo¨rg Zieren Æ Ulrich Canzler Æ Britta Bauer Æ Karl-Friedrich Kraiss

[7]	Automated Extraction of Signs from Continuous Sign Language Sentences using Iterated Conditional Modes by Sunita Nayak, Sudeep Sarkar, Barbara Loeding

[8]	Hand-Gesture Computing for the Hearing and Speech Impaired Gaurav Pradhan and Balakrishnan Prabhakaran University of Texas at Dallas Chuanjun Li Brown University

[9]	John Wiley & Sons, Crystal, D. Dictionary of Linguistics and Phonetics. The Language Library. 2011

[10]	Huenerfauth, M. Generating American sign language classifier predicates for English-to-asl machine translation. PhD thesis, University of Pennsylvania, 2006.

[11]	Rawate A.M,” A Review Paper on Sign Language Recognition System For Deaf And Dumb People using Image Processing”, ISSN: 2278-0181, March-2016

[12]	A Jeff, S Joel “Stack Overflow” Internet: https://stackoverflow.com Sep 15,2008[July.1,2019]

[13]	Lean Karlo S. Tolentino,” Static Sign Language Recognition Using Deep Learning”, Vol. 9, No. 6, December-2019

[14]	Britta Bauer and Karl-Friedrich Kraiss, Toward an Automatic Sign Language Recognition System Using Subunits, Internation Gesture Workshop (GW), Gesture and Sign Language in Human- Computer Interaction, May 2002

[15]	Dzmitry Bahdanau, Kyunghyun Cho and Yoshua Bengio, “Neural machine translation by jointly learning to align and translate,” arXiv preprint arXiv: 1409.0473, 2014

[16]	Helen Cooper, Eng-Jon Ong, Nicolas Pugeault, Richard Bowden, “Sign Language Recognition using Sub-Units,” Journal of Machine Learning Research, 13(July):2205-2231,2012
