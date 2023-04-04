#include "Engine.h"
#include<iostream>
#include<SDL.h>// used to write to screen
#include<SDL_image.h>// trying out new librarys yayyyyy
#include"texturecontrol.h"


texturecontrol* texturecontrol::s_instance = nullptr;

texturecontrol::texturecontrol()
{
}


bool texturecontrol::load(std::string id, std::string filename)
{
	SDL_Surface* surface = IMG_Load(filename.c_str()); // sets the surface variable to the texture
	if (surface == nullptr) // checking to make sure the surface loaded
	{
		std::cout << "surface load error" << SDL_GetError() << std::endl; \
		return false;
	}
	
	SDL_Texture* texture = SDL_CreateTextureFromSurface(Engine::Getinstance()->getrender(), surface);
	if (texture == nullptr) // checking to make sure the surface loaded
	{
		std::cout << "texture load error" << SDL_GetError() << std::endl; \
		return false;
	}

	m_texturemap[id] = texture; // 



	return true;
}

// i hate this function
void texturecontrol::draw(std::string id, int x, int y, int width, int height, SDL_RendererFlip flip)
{
	SDL_Rect srcRect = { 0, 0, width, height }; // reads in the source image
	SDL_Rect dstRect = { x, y, width, height }; // destanation
	SDL_RenderCopyEx(Engine::Getinstance()->getrender(), m_texturemap[id], &srcRect, &dstRect, 0, nullptr, flip );

}

void texturecontrol::drop(std::string id)
{
	SDL_DestroyTexture(m_texturemap[id]);
	m_texturemap.erase(id);
}

void texturecontrol::clean()
{
	std::map<std::string, SDL_Texture*>::iterator it;
	for (it = m_texturemap.begin(); it != m_texturemap.end(); it++)
	{
		SDL_DestroyTexture(it->second);
	}
	m_texturemap.clear();
}