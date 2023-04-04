#pragma once
#include"iobject.h"
#include"transform.h"
#include <string>
#include<SDL.h>// used to write to screen
#include<SDL_image.h>// trying out new librarys yayyyyy

// to use less code for the game object this struct is used for the basic properites when it comes to animation
struct prop
{
public:
	prop(std::string textureid, int X, int Y, int width, int height, SDL_RendererFlip flip = SDL_FLIP_NONE) 
	{	
	 std::string Textureid = textureid;
	 x = X;
	 y = Y;
	 w = width;
	 h = height;
	 Flip = flip;
	}
	std::string Textureid;
	int w, h;
	float x, y;
	SDL_RendererFlip Flip;
};

// "game" object this class will be used as a blue print for things inside the engine
class simobject : public iobject
{
public:

	simobject(prop* proptys): m_textureid(proptys->Textureid) , m_width(proptys->w), m_height(proptys->h), m_Flip(proptys->Flip)
	{
		m_transform = new transform(proptys->x, proptys->y);
	}

	
	//virtual ~simobject(){} // may not need but just incase

	virtual void draw() = 0;
	virtual void update(float delta_t) = 0;
	virtual void clean() = 0;

protected:
	transform* m_transform;
	std::string m_textureid;
	int m_width, m_height;
	SDL_RendererFlip m_Flip;
	
private:

};