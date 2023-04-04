#include<SDL.h>// used to write to screen
#include<SDL_image.h>// trying out new librarys yayyyyy
#include<iostream>
#include<cmath>
#include<vector>
#include"Engine.h"
#include"texturecontrol.h"
#include"transform.h"
#include"simobject.h"	

using namespace std;

int main(int argc, char** argv)
{

	
	
	// main game/simulation loop
	Engine::Getinstance()->init(); // calls the init method directly instead of creating a new object
	while (Engine::Getinstance()->isrunning())
	{
		Engine::Getinstance()->Events(); // checks stack for events
		Engine::Getinstance()->update(); // updates based on events 
		Engine::Getinstance()->render(); // renders to screen


	}


	Engine::Getinstance()->clean(); // call to erase all data from memory incase of unpreditable behavoir
	return 0;
}