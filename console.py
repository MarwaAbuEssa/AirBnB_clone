#!/usr/bin/python3
"""Defines the HBNBCommand console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(argument):
    curly_braces = re.search(r"\{(.*?)\}", argument)
    brackets = re.search(r"\[(.*?)\]", argument)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(argument)]
        else:
            leftexer = split(argument[:brackets.span()[0]])
            retleft = [i.strip(",") for i in leftexer]
            retleft.append(brackets.group())
            return retleft
    else:
        leftexer = split(argument[:curly_braces.span()[0]])
        retleft = [i.strip(",") for i in leftexer]
        retleft.append(curly_braces.group())
        return retleft


class HBNBCommand(cmd.Cmd):
    """Defines AirnBnB command interpreter.

    Attributes:
        prompt (str): command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """an empty line."""
        pass

    def default(self, argument):
        """if input is invalid"""
        cmd_dict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", argument)
        if match is not None:
            argleft = [argument[:match.span()[0]], argument[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argleft[1])
            if match is not None:
                command = [argleft[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in cmd_dict.keys():
                    call = "{} {}".format(argleft[0], command[1])
                    return cmd_dict[command[0]](call)
        print("*** Unknown syntax: {}".format(argument))
        return False

    def do_quit(self, argument):
        """Quit to exit."""
        return True

    def do_EOF(self, argument):
        """EOF to exit."""
        print("")
        return True

    def do_create(self, argument):
        """Usage: create <class>
        init new class with id.
        """
        argleft = parse(argument)
        if len(argleft) == 0:
            print("** class name missing **")
        elif argleft[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(argleft[0])().id)
            storage.save()

    def do_show(self, argument):
        """Usage: show <class> <id> or <class>.show(<id>)
        Get string  of a class by id.
        """
        argleft = parse(argument)
        objdict = storage.all()
        if len(argleft) == 0:
            print("** class name missing **")
        elif argleft[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argleft) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argleft[0], argleft[1]) not in objdict:
            print("** no instance found **")
        else:
            print(objdict["{}.{}".format(argleft[0], argleft[1])])

    def do_destroy(self, argument):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class by id."""
        argleft = parse(argument)
        objdict = storage.all()
        if len(argleft) == 0:
            print("** class name missing **")
        elif argleft[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argleft) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argleft[0], argleft[1]) not in objdict.keys():
            print("** no instance found **")
        else:
            del objdict["{}.{}".format(argleft[0], argleft[1])]
            storage.save()

    def do_all(self, argument):
        """Usage: all or all <class> or <class>.all()
        Display all instances of a class.
        When no class , get all objects."""
        argleft = parse(argument)
        if len(argleft) > 0 and argleft[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(argleft) > 0 and argleft[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(argleft) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_count(self, argument):
        """Usage: count <class> or <class>.count()
        Get number of objects of a class."""
        argleft = parse(argument)
        count = 0
        for obj in storage.all().values():
            if argleft[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, argument):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Add/Update a class instance by id
        an attribute key/value dictionary."""
        argleft = parse(argument)
        objdict = storage.all()

        if len(argleft) == 0:
            print("** class name missing **")
            return False
        if argleft[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(argleft) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argleft[0], argleft[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(argleft) == 2:
            print("** attribute name missing **")
            return False
        if len(argleft) == 3:
            try:
                type(eval(argleft[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argleft) == 4:
            obj = objdict["{}.{}".format(argleft[0], argleft[1])]
            if argleft[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[argleft[2]])
                obj.__dict__[argleft[2]] = valtype(argleft[3])
            else:
                obj.__dict__[argleft[2]] = argleft[3]
        elif type(eval(argleft[2])) == dict:
            obj = objdict["{}.{}".format(argleft[0], argleft[1])]
            for k, v in eval(argleft[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
