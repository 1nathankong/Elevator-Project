##elevator software application
class Elevator:
    def __init__(self):
        self.current_floor = None  # Default starting floor
        self.elevator_direction = None
        self.num_floors = 4
        self.floor_input = []

    def set_direction(self, direction):
        if direction == 1:
            self.elevator_direction = "up"
        elif direction == 0:
            self.elevator_direction = "down"
        else:
            self.elevator_direction = "invalid direction"
    
    def get_direction(self):
        return self.elevator_direction

    def set_current_floor(self, first_floor_clicked: bool, second_floor_clicked: bool, third_floor_clicked: bool, fourth_floor_clicked: bool):
        if first_floor_clicked:
            self.current_floor = 1
        if second_floor_clicked:
            self.current_floor = 2
        if third_floor_clicked:
            self.current_floor = 3
        if fourth_floor_clicked:
            self.current_floor = 4

    def get_current_floor(self):
        return self.current_floor
    
    def set_floor_input(self, first_floor_clicked: bool, second_floor_clicked: bool, third_floor_clicked: bool, fourth_floor_clicked: bool): ##one implementation is that i can reverse the for loop 
        if first_floor_clicked:
            self.floor_input.append(1)
        if second_floor_clicked:
            self.floor_input.append(2)
        if third_floor_clicked:
            self.floor_input.append(3)
        if fourth_floor_clicked:
            self.floor_input.append(4)

    def upward_valid(self):
        min = self.floor_input[0]
        if self.get_current_floor() < min:
            return True
        return False
    
    def downward_valid(self):
        max = self.floor_input[0]
        if self.get_current_floor() > max:
            return True
        return False
    
    def is_empty(self):
        if len(self.floor_input) == 0:
            return True
        else:
            return False
    
    def only_one_floor(self):
        if len(self.floor_input) == 1:
            return True
        else:
            return False


    def get_floor_input(self):
        return self.floor_input
    
    def four_floor_operation(self, direction: int, first_floor_clicked: bool, second_floor_clicked: bool, third_floor_clicked: bool, fourth_floor_clicked: bool):
        ##first get the direction of the elevator
        self.set_direction(direction)
        self.set_floor_input(first_floor_clicked, second_floor_clicked, third_floor_clicked, fourth_floor_clicked)
        
        #print(self.get_floor_input())
        
        #if the direction is upward, then when organizing the inputs, sort in ascending order, if the direction is downward, then the sort is in decending order
        if self.get_direction() == "up":
            if self.is_empty():
                print("No inputs clicked")
            else:
                self.get_floor_input()
                if self.only_one_floor():
                    print("Stay on Floor " + str(self.floor_input[0]) + "\n")
                else:
                    for i in self.floor_input:
                        if self.upward_valid():
                            self.current_floor = i
                        start_floor = self.floor_input[0]
                    print(self.get_floor_input())
                    print("start on Floor " + str(start_floor))
                    print("going up to Floor " + str(self.current_floor) + "\n")

            #find current state 
            # if current state is less than input and direction is upward move to the destination input floor. use bubble sort
        elif self.get_direction() == "down":
            if self.is_empty():
                print("No inputs clicked")
            else:
                self.floor_input.sort(reverse=True)
                self.get_floor_input()
                if self.only_one_floor():
                    print("Stay on Floor " + str(self.floor_input[0]) + "\n")
                else:
                    
                    for i in self.floor_input:
                        if self.downward_valid():
                            self.current_floor = i
                        start_floor = self.floor_input[0]
                    print(self.get_floor_input())
                    print("start on Floor " + str(start_floor))
                    print("going down to Floor " + str(self.current_floor) + "\n")
        else:
            print("invalid destination, go either up or down")
        # create a variable to show the state of the elevator changing. 
        #nothing will happen if no inputs are pressed. 

        #edge cases

        ## case 1 ##
        #otherwise do not do anything
        # since there could be multiple input floors keep updating the state as you keep moving

        ## case 2 ## 
        # if current state is more than input and direction is downward move to destination input floor.  use bubble sort
        # since there could be multiple input floors keep updating the state as you keep moving
        #otherwise do nothing

        ## case 3 ## nothing can be pressed at all and the elevator does nothing. 

        ## case 4 ## adding to elevator inputs

        # check if elevator is in same direction, if so check if floor input would be in valid floor range, if so then add to list then sort if not dont do anything. 

def test_floor_elevator():
    tester = Elevator()
    """
    elevator_two_floors.two_floor_operation(first_floor_clicked = False,second_floor_clicked = False, door_closed_clicked = False)
    elevator_two_floors.two_floor_operation(first_floor_clicked = False,second_floor_clicked = False, door_closed_clicked = True)
    elevator_two_floors.two_floor_operation(first_floor_clicked = False, second_floor_clicked = True, door_closed_clicked = False)
    elevator_two_floors.two_floor_operation(first_floor_clicked = False, second_floor_clicked = True, door_closed_clicked = True)
    elevator_two_floors.two_floor_operation(first_floor_clicked = True, second_floor_clicked = False, door_closed_clicked = False)
    elevator_two_floors.two_floor_operation(first_floor_clicked = True, second_floor_clicked = False,door_closed_clicked = True)
    elevator_two_floors.two_floor_operation(first_floor_clicked = True,second_floor_clicked = True, door_closed_clicked = False)
    elevator_two_floors.two_floor_operation(first_floor_clicked = True,second_floor_clicked = True, door_closed_clicked= True)
    """
    for direction in [0, 1]:
        for first_floor_clicked in [False, True]:
            for second_floor_clicked in [False, True]:
                for third_floor_clicked in [False, True]:
                    for fourth_floor_clicked in [False, True]:
                        print(f"Testing with direction = {direction}, "f"first_floor_clicked={first_floor_clicked}, "f"second_floor_clicked={second_floor_clicked}, "f"third_floor_clicked={third_floor_clicked}, "f"fourth_floor_clicked={fourth_floor_clicked}")
                        tester.four_floor_operation(direction, first_floor_clicked, second_floor_clicked, third_floor_clicked, fourth_floor_clicked)
                        tester.floor_input.clear()
    #tester.four_floor_operation(.5, False,False, True, True)
test_floor_elevator()