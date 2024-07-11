% Dynamic predicates used
% to store the contacts names
:- dynamic is_contact/1.

% Main loop:
% - reads a command
% - processes the command
% - loops ;)
main :- 
    read_command(Command),
    process_command(Command),
    main.

% Predicate reading command from the standard input
% Available commands:
% - "add" - add contact
% - "del" - remove contact
% - "list" - print all the contacts
% - "help" - show help
% - "exit" - exit the program
read_command(Command) :- read(Command).

% Predicate responsible for the 'help' command
% You need to create four more `process_command` clauses,
% In case user choose an incorrect command, the program should
% inform user about his mistake and continue working
process_command(help) :- 
    writeln("Available commands:"),
    writeln("- 'add' - add contact"),
    writeln("- 'del' - remove contact"),
    writeln("- 'list' - print all the contacts"),
    writeln("- 'help' - show help"),
    writeln("- 'exit' - exit the program").    

% @tbd: write missing clauses to handle all the commands!

process_command(add) :-
    writeln("Add contact:"),
    read(Contact),
    add_contact(Contact).

add_contact(Contact):-
    \+ is_contact(Contact),
    assert(is_contact(Contact)),
	writeln("Contact added").

add_contact(Contact):-
    is_contact(Contact),
    writeln("This contact is already in your list").

process_command(del) :-
    writeln("Delete contact:"),
    read(Contact),
    delete_contact(Contact).

delete_contact(Contact) :-
    is_contact(Contact),
    retractall(is_contact(Contact)),
    writeln("Contact deleted").

delete_contact(Contact) :-
    \+ is_contact(Contact),
    writeln("This contact doesn't exist").


process_command(list) :-
    writeln("List of contacts:"),
    list_contacts.

list_contacts :- 
    is_contact(Contact),
    writeln(Contact).

process_command(exit) :- 
    writeln("Exit."),
    !,
    fail.

process_command(Command):-
    writeln("Incorrect command").



