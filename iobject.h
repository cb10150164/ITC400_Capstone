#pragma once

class iobject
{
public:
	virtual void draw() = 0;
	virtual void update(float delta_t) = 0;
	virtual void clean() = 0;
};