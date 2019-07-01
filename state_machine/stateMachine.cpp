/******************************************************************************
This is an shell-based program. There are no classes and the file contains a 
main() function. The program execution starts and ends here. 
*******************************************************************************/

#include <iostream>
#define correctAmount 20

using namespace std;

enum State 
{
	LOCKED,
	UNLOCKED,
	BROKEN
};

enum Event 
{
	NOEVENT,
	COIN,
	PASS,
	FIXED,
	FAILED
};

static int totalAmount = 0;
static State currentState = LOCKED;

Event getEvent()
{
	int event = -1;
	while (event < 0 || event > 5)
	{
		std::cout << "1 - COIN, 2 - PASS, 3 - FIXED, 4 - FAILED." << std::endl << "Enter an occured event number: ";
		std::cin >> event;
	}

	return static_cast<Event>(event);
}

void exitState(State state)
{
	switch (state)
	{
	case LOCKED:
		totalAmount = 0;
		break;
	default:
		break;
	}
}

void entryState(State state) 
{
	// currentState = state;
	switch (state)
	{
	case LOCKED:
		std::cout << "The machine entered the state locked" << std::endl;
		currentState = state;
		break;
	case UNLOCKED:
		std::cout << "The machine entered the state unlocked" << std::endl;
		currentState = state;
		break;
	case BROKEN:
		std::cout << "The machine entered the state broken" << std::endl;
		currentState = state;
		break;
	default:
		break;
	}
}

void accumulate()
{
	int insertedCoins = 0;

	std::cout << "Please insert " << correctAmount - totalAmount << " coins" << std::endl;
	std::cout << "Amount of inserted coins: ";
	std::cin >> insertedCoins;
	totalAmount += insertedCoins;

	if (totalAmount >= correctAmount) 
	{
		exitState(LOCKED);
		entryState(UNLOCKED);
	}
}


int main()
{
	entryState(currentState);
	Event event = NOEVENT;

	while (true) 
	{
		event = getEvent();
		switch (currentState)
		{
		case LOCKED:
			if (COIN == event)
				accumulate();
			else if (FAILED == event)
			{
				exitState(LOCKED);
				entryState(BROKEN);
			}
			else
				std::cout << "This event is not allowed" << std::endl;
			break;

		case UNLOCKED:
			if (COIN == event)
				std::cout << "Thank you!" << std::endl;
			else if (PASS == event)
			{
				exitState(UNLOCKED);
				entryState(LOCKED);
			}
			else if (FAILED == event)
			{
				exitState(UNLOCKED);
				entryState(BROKEN);
			}
			else
				std::cout << "This event is not allowed" << std::endl;
			break;

		case BROKEN:
			if (FIXED == event) 
			{
				exitState(BROKEN);
				entryState(LOCKED);
			}
			else
				std::cout << "This event is not allowed" << std::endl;
			break;

		default:
			break;
		}
	}
}
