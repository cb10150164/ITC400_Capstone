#pragma once

#include<string>
#include<SDL.h>
#include<map>

class texturecontrol
{
public:
	static texturecontrol* getinstance()
	{
		if (s_instance == nullptr) { s_instance = new texturecontrol(); }	return s_instance;
	}

	bool load(std::string id, std::string filename);
	void drop(std::string id);
	void clean();

	void draw(std::string id, int x, int y, int width, int height, SDL_RendererFlip flip = SDL_FLIP_NONE);

private:
	texturecontrol();
	static texturecontrol* s_instance;
	texturecontrol(const texturecontrol&) = delete; // These lines disallow copying and assignment 
	texturecontrol& operator=(const texturecontrol&) = delete;
	std::map<std::string, SDL_Texture*> m_texturemap;

};