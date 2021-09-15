

def set_space(client, space_name):
    if client.set_space(space_name):
        print(f'#> Space set -> {client.space}')

def help(client):
    print(
    """
    === HELP ===
    Commands:
        Info:
            [region] -> Get region name of client session.
            [space] -> Get the current space.
        Set:
            [set space <space_name>] -> Set/change the client's current space.
        Other:
            [exit] -> Quit the client shell.
    """
    )

def shell(client):
    print(f"\n=== {client} Shell ===")
    print(f"#> First time? Try 'help'.")
    print(f"#> !! The shell in development and has limited functionality. !!")

    cmd = ''
    exit = False

    while not exit:

        cmd = input(f"{client.region}/{client.space} #> ").split()

        try:
            # Command Tree
            if cmd[0].lower() in ['exit', 'quit', 'exit()', 'quit()']:
                exit = True
            elif cmd[0].lower() in ['help']: help(client)
            elif cmd[0].lower() in ['region', 'region name', 'server']:
                print(f'#> Region: {client.region}')
            elif cmd[0].lower() in ['space', 'space name']:
                print(f'#> Space: {client.space}')
            elif cmd[0].lower() in ['set']:
                if len(cmd) > 1:
                    if cmd[1].lower() in ['space']:
                        if len(cmd) == 3:
                            set_space(client, cmd[2])
                        else:
                            print("#> [set space] Requires a 'space name' argument.")
                    else:
                        print(f"#> [{cmd[1]}] is not a valid argument.")
                else: 
                    print("#> [set] requires additional arguments.")
            else:
                print(f"#> [{cmd[0]}] is invalid, try 'help' instead.")

        finally:
            pass

    print("#> Goodbye")
