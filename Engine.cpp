#include "Engine.h"
#include<iostream>
#include<SDL.h>// used to write to screen
#include<SDL_image.h>// trying out new librarys yayyyyy
#include<cmath>
#include<vector>
#include"texturecontrol.h"

Engine* Engine::s_instance = nullptr;

Engine::Engine()
{

}

bool Engine::init()
{
	//m_isrunning = true;
	if (SDL_Init(SDL_INIT_VIDEO) != 0)// makes sure sdl is working correctly
	{
		std::cout << "SDL ERROR 0" << SDL_GetError() << std::endl;
		return false;
	}
	if (SDL_Init(SDL_INIT_AUDIO) !=  0 ) // checks to make sure audio libray is working correctly
	{
		std::cout << "SDL Error Audio" << SDL_GetError() << std::endl;
		return false;
	}
	if (!(IMG_Init(IMG_INIT_PNG| IMG_INIT_JPG)))// checks to make sure img_init in sdl_image works
	{
		std::cout << "SDL_IMAGE error" << SDL_GetError() << std::endl;
		return false;
	}
	
	// this code will create and then check to make sure the window and render variables can be created and used
	m_window = SDL_CreateWindow("test", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, screen_w, screen_h,9);
	if(m_window == nullptr)
	{
		std::cout << "window creation error" << SDL_GetError() << std::endl;
		return false;
	}
	m_render = SDL_CreateRenderer(m_window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
	if (m_render == nullptr)
	{
		std::cout << "rendor creation error" << SDL_GetError() << std::endl;
		return false;
	}



	m_isrunning = true;
	return m_isrunning;
}

bool Engine::clean()
{
	texturecontrol::getinstance()->clean();
	SDL_DestroyRenderer(m_render);
	SDL_DestroyWindow(m_window);
	IMG_Quit();
	SDL_Quit();


	return true;
}

void Engine::quit()
{
	m_isrunning = false;
}

void Engine::update()
{
	std::cout << "updating" << std::endl;

}

void Engine::render()
{
	std::cout << "rendering" << std::endl;
	
}

void Engine::Events() 
{
	//std::cout << "eventing" << std::endl;
	SDL_Event event;
	SDL_PollEvent(&event);

	/*
	switch (event.type)
	{
	case SDL_QUIT():
			 quit();
			 break;
		
	}
	*/


}