def is_palindrome(s):
    return s == s[::-1]

# Test
test_string = "radar"
print(is_palindrome(test_string))
