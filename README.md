# TUBER

TUBER is a web application that allows students to request on-demand tutoring help from nearby students. 

# Overview
TUBER allows the user to login to their account, switch between the mentor (tutor) and the student view, request mentors and view/accept requests for tutoring sessions in your area. The application also supports periodic location updates in the database for the tutors to provide up-to-date matching based on geographic proximity.

<img src="src/img1.JPG" width="550" height ="275"><nobr>
<img src="src/img2.JPG" width="550" height ="275"><nobr>
<img src="src/img3.JPG" width="550" height ="275"><nobr>
<img src="src/Screen Shot 2019-05-13 at 23.44.59.png" width="550" height ="275"><nobr>


# curl command for request service

'''
curl 'http://localhost:7777/getMentors?ltude=-74.06725&latitude=40.747&subject=cs'
'''
