##elevator software application
class Elevator:
    def __init__(self):
        self.floor_state = 1  # Default starting floor
        self.elevator_direction = -1 ## 0 would mean going down 1 would mean going up

    def two_floor_operation(self, first_floor_clicked: bool, second_floor_clicked: bool, door_closed_clicked: bool):

        if (not first_floor_clicked and second_floor_clicked and door_closed_clicked) or (self.floor_state == 1 and first_floor_clicked and second_floor_clicked and door_closed_clicked):
            self.floor_state = 2
            print("Elevator on: Floor " + str(self.floor_state))
        elif (first_floor_clicked and not second_floor_clicked and door_closed_clicked) or (self.floor_state == 2 and first_floor_clicked and second_floor_clicked and door_closed_clicked):
            self.floor_state = 1
            print("Elevator on Floor " +  str(self.floor_state))
        else:
            print("Staying on current floor: " + str(self.floor_state))
def test_two_floor_elevator():
    elevator_two_floors = Elevator()
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
    for first_floor_clicked in [False, True]:
        for second_floor_clicked in [False, True]:
            for door_closed_clicked in [False, True]:
                elevator_two_floors.two_floor_operation(first_floor_clicked, second_floor_clicked, door_closed_clicked)
test_two_floor_elevator()