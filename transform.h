#pragma once
#include"vectormath.h"

class transform
{
public:
	float x, y;

	transform(float X = 0,  float Y = 0) :x(X), y(Y) {}

private:
	inline void transform_x(float X) { x+= X; }
	inline void transform_y(float Y) { y+= Y; }
	inline void tranlate(vectormath v) { x += v.X; y += v.Y; }

};
