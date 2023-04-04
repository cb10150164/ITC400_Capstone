#pragma once



class vectormath
{
public:
	float X, Y;

	vectormath(float x = 0, float y = 0) :X(x), Y(y) {}// vector constucter

	inline vectormath operator+(const vectormath& v2) const // addtion method
	{
		return vectormath(X + v2.X, Y + v2.Y);
	}

	inline vectormath operator-(const vectormath & v2) const // subtraction method
	{
		return vectormath(X - v2.X, Y - v2.Y);
	}

	//inline vectormath operator*(const vectormath& v2) const
	//{
	//	return vectormath(X * scaler , Y * scaler );
	//}

private:




};