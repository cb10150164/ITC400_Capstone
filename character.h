#pragma once

#include"simobject.h"
#include<string>

class character : public simobject
{
public:
	character(prop* proptys): simobject(proptys){}

	virtual void draw() = 0;
	virtual void clean() = 0;
	virtual void update(float dt) = 0;

protected:
	std::string m_name;
};