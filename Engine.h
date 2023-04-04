#pragma once
#include<SDL.h>// used to write to screen
#include<SDL_image.h>// trying out new librarys yayyyyy
#include<iostream>
#include<cmath>


#define screen_w 900
#define screen_h 600


class Engine
{
public:			// get function that will return what instance is set to and prevents the eninge from being recreated inside the memory
	static Engine* Getinstance() {if (s_instance == nullptr){s_instance = new Engine();}	return s_instance;}
	//virtual ~Engine();
	bool init();
	bool clean();
	
	void update();
	void render();
	void Events();
	void quit();

	inline bool isrunning() { return m_isrunning; } // memory saving code
	inline SDL_Renderer* getrender() { return m_render; }


private:
	Engine(); // main contruster made private for secuirty 
	Engine(const Engine&) = delete; // These lines disallow copying and assignment 
	Engine& operator=(const Engine&) = delete; //of the singleton instance by deleting the copy constructor and the assignment operator.
	
	static Engine* s_instance;  // all variables that will have assiocation with static properties 
								// will be labeled with prefix s_
	bool m_isrunning;
	SDL_Window* m_window;
	SDL_Renderer* m_render;


};