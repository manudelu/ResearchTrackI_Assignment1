############################################## FIRST ASSIGNMENT RESEARCH TRACK ######################################################

from __future__ import print_function

import time
from sr.robot import *

a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""

silver = True;
""" boolean: variable for letting the robot know if it has to look for a silver or for a golden marker"""

R = Robot()
""" Instance of the Class Robot """

list_golden_token = []
""" List that store the golden tokens"""

list_silver_token = []
""" List that store the silver tokens"""

############################################## FUNCTIONS ######################################################

def drive(speed, seconds):
    """
    Function for setting a linear velocity:
    Allows the robot to move into a straight line for a certain time and with a defined speed
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity:
    Allows the robot to turn on its axis
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_silver_token(list_silver_token):
    """
    Function to find the closest SILVER token that has not been already paired
    
    Args: list_silver_token : the list of codes (silver tokens) that have already been paired

    Returns:
	dist (float): distance of the closest silver token (-1 if no silver token is detected)
	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
	code (int): numeric code of the token
    """
    dist=100  # Max distance that the robot can see
    
    for token in R.see():  # Iterate through all the detected token
    
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER:  # Check if this is the closest silver token detected
        
            for i in list_silver_token:  # Check that this token has not already been paired 
                if i == token.info.code:  # If it is already been paired -> break
                    break
            else:  # If it is not already been paired -> Update the distance, the angle and the code values corresponding to this silver token
                dist=token.dist
	        rot_y=token.rot_y
	        code = token.info.code
    if dist==100:  # If it did not find any unpaired golden token -> return -1
	return -1, -1, -1
    else:  # If it did find any unpaired golden token -> return the corresponding values
   	return dist, rot_y, code

def find_golden_token(list_golden_token):
    """
    Function to find the closest GOLDEN token that has not already been paired
    
    Args: list_golden_token : the list of codes (golden tokens) that have already been paired

    Returns:
	dist (float): distance of the closest golden token (-1 if no golden token is detected)
	rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
	code (int): numeric code of the token
    """
    dist=100  # Max distance that the robot can see
    
    for token in R.see():  # Iterate through all the detected token
    
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD:  # Check if this is the closest golden token detected
        
            for i in list_golden_token:  # Check that this token has not already been paired 
                if i == token.info.code:  # If it is already been paired -> break
                    break
            else:  # If it is not already been paired -> Update the distance, the angle and the code values corresponding to this golden token
                code = token.info.code
                dist=token.dist
	        rot_y=token.rot_y
	        
    if dist==100:  # If it did not find any unpaired silver token -> return -1
	return -1, -1, -1
    else:  # If it did find any unpaired silver token -> return the corresponding values
   	return dist, rot_y, code
  
def MovetoSilver():
    """
    Function to approach and grab the SILVER token that has not already been paired
    
    The idea is to find the silver token in the robot's field of view, approach it and then grab it 
    """
    dist_silver, rot_y_silver, code_silver = find_silver_token(list_silver_token) 
       
    if dist_silver == -1:  # If no silver token is detected, we make the robot turn until we find one
        print("I don't see any token!!")
        turn(+10, 1)
    elif rot_y_silver < -a_th: # If the robot is not well aligned with the token, we move it on the left
        print("Left a bit...")
     	turn(-2, 0.5)
    elif rot_y_silver > a_th:  # If the robot is not well aligned with the token, we move it on the right
   	print("Right a bit..")
   	turn(+2, 0.5)
    elif dist_silver < d_th:  # If we are close to the token, then we grab it
	print("Found it!!")
	
	if R.grab():
	    print("Gotcha!!")
	    list_silver_token.append(code_silver)  # Silver list updated with the codes of tokens already paired
	    print("Silver Token List: " ,list_silver_token)
	    global silver
	    silver = not silver  # Silver = False: so that in the next step we search for a new unpaired golden token
	       
    else:  # If the robot is well aligned with the token, we go forward
	 print("Forward...")
	 drive(30, 0.3)
	    
def MovetoGolden():
    """
    Function to approach the GOLDEN token that has not already been paired and release the SILVER token near it
    
    The idea is to find the golden token in the robot's field of view, approach it and then release the silver token near it 
    """
    dist_golden, rot_y_golden, code_golden = find_golden_token(list_golden_token) 
	       
    if dist_golden == -1:  # If no golden token is detected, we make the robot turn until we find one
	 print("I don't see any token!!")
	 turn(+10, 1)
    elif rot_y_golden < -a_th: # If the robot is not well aligned with the token, we move it on the left 
         print("Left a bit...")
     	 turn(-2, 0.5)
    elif rot_y_golden > a_th:  # If the robot is not well aligned with the token, we move it on the right
   	 print("Right a bit..")
   	 turn(+2, 0.5)
    elif dist_golden < 1.5*d_th:  # If we are close to the token, then we release it  
	 print("Found it!!")
	 
	 if R.release():
	    print("Paired!!")
	    list_golden_token.append(code_golden)  # Golden list updated with the codes of tokens already paired 
	    print("Golden Token List: ", list_golden_token)
	    global silver
	    silver = not silver  # Silver = True: so that in the next step we search for a new unpaired silver token
	    drive(-50,2)  # We drive back with the robot (not essential)
	 
    else:  # If the robot is well aligned with the token, we go forward
         print("Forward...")
         drive(30, 0.3) 
         
def Mission_Complete():
    """
    Function that ends the program (exit the while loop) when all the golden tokens are paired
    """
    if len(list_golden_token) == 6: # If we have already paired the six golden tokens, exit the program
	 print("Mission Complete!")
	 exit()




############################################## MAIN ######################################################

# The idea is to have an infinite loop to make the robot move continuously (until all of the tokens are paired)
# The first step is to find the silver token in the robot's field of view, approach it and then grab it 
# The second step is to find the golden token in the robot's field of view, approach it and then release the silver token near it
# Then, the robot will follow this process until all of the tokens are paired

while 1:
  
   if silver:  # If silver = True: we look for a silver token that is not already been paired
      
       MovetoSilver()
	    
   else:  # If silver = False: we look for a golden token that is not alreafy been paired
     
       MovetoGolden()
       
   Mission_Complete()
                   
