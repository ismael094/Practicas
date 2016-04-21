def fibonnaci(n):
	if n<=1:
		return n
	else:
		return fibonnaci(n-1)+fibonnaci(n-2)

print fibonnaci(3)
