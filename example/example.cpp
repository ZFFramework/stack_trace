// Copyright 2007 Edd Dawson.
// Distributed under the Boost Software License, Version 1.0.
// (See accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

#include <algorithm>
#include <iostream>
#include <iterator>

#include <dbg/stack.hpp>

template<unsigned Depth>
struct recurser
{
	static void f()
	{
		recurser<Depth - 1>::f();
	}
};

template<>
struct recurser<0>
{
	static void f()
	{
		dbg::stack s;
		std::copy(s.begin(), s.end(), std::ostream_iterator<dbg::stack_frame>(std::cout, "\n"));
	}
};


void e()
{
	dbg::stack s;
	std::copy(s.begin(), s.end(), std::ostream_iterator<dbg::stack_frame>(std::cout, "\n"));
}

void d() { e(); }
void c() { d(); }
void b() { c(); }
void a() { b(); }

int main()
{
	std::cout << "Testing template functions:\n";
	recurser<10>::f();

	std::cout << "\nTesting regular functions:\n";
	a();

	return 0;
}
