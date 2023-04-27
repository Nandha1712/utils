def get_object_to_explore():
    from azure.messaging.webpubsubservice import WebPubSubServiceClient

    hub_name = "***"
    access_key_value = "*****"
    pubsub_name = "****"

    cxn_str = f"Endpoint=https://{pubsub_name}.webpubsub.azure.com;AccessKey={access_key_value};Version=1.0;"
    service = WebPubSubServiceClient.from_connection_string(cxn_str, hub=hub_name)
    return service


# Any python object can be given in the next line. 
object_to_explore = get_object_to_explore()


def add_ab(a: int, b: int) -> int:
    """
    Sample function used for example purpose
    Adds 2 given numbers and returns the result

    Args:
        a (int): Input number 1
        b (int): Input number 2

    Returns:
        int: the added result
    """
    c = a + b
    return c


def get_methods(_object, spacing=20):
    """
    This function prints the methods present inside the given object.

    This function is created in reference to the SO answer.
    https://stackoverflow.com/questions/34439/finding-what-methods-a-python-object-has/34452#34452

    Args:
        _object: The python object whose methods should be displayed
        spacing: Number of spacing required during printing the results

    Returns:

    """
    method_list = []
    # Gathering the methods present inside the given object
    for method_name in dir(_object):
        try:
            if callable(getattr(_object, method_name)):
                method_list.append(str(method_name))
        except Exception as exp:
            print(exp)
            method_list.append(str(method_name))

    # Processing and printing the result
    process_func = (lambda s: ' '.join(s.split())) or (lambda s: s)
    for method in method_list:
        try:
            print(str(method.ljust(spacing)) + ' ' +
                  process_func(str(getattr(_object, method).__doc__)[0:90]))
        except Exception as exp:
            print(exp)
            print(method.ljust(spacing) + ' ' + ' getattr() failed')


print(f"About to print the methods present in {object_to_explore}")
get_methods(object_to_explore)
print("\n\n\n\n\n =============== \n\n")


# print(object_to_explore.send_to_user.__doc__)
print(add_ab.__doc__)
print("\n\n\n\n\n *************** \n\n")

import inspect
lines = inspect.getsource(add_ab)
print(lines)

# lines = inspect.getsource(object_to_explore.send_to_user)
# print(lines)

print("\n\n\n\n\n ################# \n\n")
