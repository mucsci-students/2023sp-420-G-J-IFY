# Authors: Francesco Spagnolo
# Course : CSCI 420
# Modified Date: 2/1/2023
# A module for the showing rank based on points and point threshold

# Params: points: takes points as an int, pointThresh is a list of ints 
# Finds the rank that the player is by basis of points and the point threshold
def showStatus(points, pointThresh):
    #checking every point threshold here
    rank = "Beginner"
    if 0 < points < pointThresh[0]: 
        return rank 
    elif pointThresh[0] <= points < pointThresh[1]: 
        rank = "Novice"
        return rank 
    elif pointThresh[1] <= points < pointThresh[2]: 
        rank = "Okay"
        return rank 
    elif pointThresh[2] <= points < pointThresh[3]: 
        rank = "Good"
        return rank 
    elif pointThresh[3] <= points < pointThresh[4]: 
        rank = "Very Good"
        return rank 
    elif pointThresh[4] <= points < pointThresh[5]: 
        rank = "Superb"
        return rank 
    elif pointThresh[5] <= points < pointThresh[6]: 
        rank = "Fabulous"
        return rank 
    elif pointThresh[6] <= points < pointThresh[7]: 
        rank = "Exceptional"
        return rank 
    elif pointThresh[7] <= points < pointThresh[8]: 
        rank = "Genius"
        return rank
    return rank #just in case, undershoot and stay at beginner
