#!/usr/bin/python3
"""The console AirBnB"""
import cmd
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.city import City
from models.engine.file_storage import FileStorage
from models import storage


class HBNBCommand(cmd.Cmd):
    """The class for cmd"""
    prompt = "(hbnb) "
    instances = ["BaseModel", "User", "State",
                 "City", "Amenity", "Place", "Review"]

    def emptyline(self):
        """
        Empty line
        """
        pass

    def do_EOF(self, arg):
        """
        Quit command to exit the program
        """
        return True

    def do_quit(self, arg):
        """
        Quit command to exit the program
        """
        return True

    def do_create(self, arg):
        """
        Creates a new instance of BaseModel
        """
        args = arg.split()

        if len(args) < 1:
            print("** class name missing **")
        elif arg in self.instances:
            new_obj = eval(arg + '()')
            new_obj.save()
            print(new_obj.id)
        else:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """
        Prints the string representation of
        an instance based on the class name
        """
        args = arg.split()
        if len(args) < 1:
            print("** class name missing **")
        elif args[0] not in self.instances:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = args[0] + '.' + args[1]
            all_objects = storage.all()
            if key in all_objects:
                print(all_objects[key])
            else:
                print("** no instance found **")

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name and id
        """
        args = arg.split()
        all_objects = storage.all()

        if len(args) < 1:
            print("** class name missing **")
        elif args[0] not in self.instances:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = args[0] + '.' + args[1]
            if key in all_objects:
                del all_objects[key]
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, arg):
        """
        Prints all string representation of
        all instances based or not on the class name
        """
        list_instan = []
        args = arg.split()
        all_objects = storage.all()
        if len(args) == 0:
            for key in all_objects:
                list_instan.append(all_objects[key].__str__())
            print(list_instan)
        else:
            if args[0] in self.instances:
                for key in all_objects:
                    if args[0] in key:
                        list_instan.append(all_objects[key].__str__())
                    print(list_instan)
            else:
                print("** class doesn't exist **")

    def do_update(self, arg):
        """
        Updates an instance based on the class name and id
        """
        args = arg.split()
        all_objects = storage.all()

        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.instances:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = args[0] + '.' + args[1]
            if key in all_objects:
                if len(args) < 3:
                    print("** attribute name missing **")
                elif len(args) < 4:
                    print("** value missing **")
                else:
                    obj_dict = all_objects[key].to_dict()
                    my_obj = all_objects[key]
                    if args[2] in obj_dict:
                        cast = type(my_obj.args[3])
                        cast(args[3])
                    setattr(my_obj, args[2], args[3])
                    my_obj.save()
            else:
                print("** no instance found **")


if __name__ == '__main__':
    """console loop"""
    HBNBCommand().cmdloop()
