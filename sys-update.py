#!/usr/bin/env python3

import sys, subprocess, time
from tkinter import *
from tkinter import ttk

class App_Window():
    """Class to hold representation on the tkinter program itself. Making it a class alleviates some pain
    with programming in other regards."""
    
    def __init__(self, parent):
        """Creating the tkinter frames, starting with a default info-screen as the content."""
        
        self.my_parent = parent
        
        self.currentSystem = Csys()
        self.user = Suser()
        
        # Creating all of the frames and labels
        self.content_frame = ttk.Frame(parent)
        self.content = ttk.Frame(self.content_frame)
        self.command_frame = ttk.Frame(parent, borderwidth=5)
        self.welcome_label = ttk.Label(self.content, text="Welcome to Sys-Update", anchor = CENTER)
                
        self.text_label = ttk.Label(self.content, text="The last detected update was: {0}\n".format(self.currentSystem.get_last_update(self.user.name)) \
                                    + "Would you like to procced with an update?".center(70, ' '), anchor = CENTER)
        
        # Creating all of the buttons
        self.yes_button = ttk.Button(self.command_frame, text = "Update")
        self.no_button = ttk.Button(self.command_frame, text = "No")
        self.separator = ttk.Separator(self.command_frame, orient=HORIZONTAL)
    
        # Binding all of the buttons (what they do)
        self.yes_button.bind("<Button-1>", self.proceed_update) # when left mouse click go to func proceed update
        self.user_string = StringVar()
        self.user_string.set('Empty') # This is used to check if going straight to show info and no update!
        self.completedSwitch = StringVar()
        self.completedSwitch.set('')
        self.no_button.bind("<Button-1>", self.show_info)

        #Putting the frames onto the root window (displaying them also)
        self.content_frame.grid(column=0, row=0)
        self.command_frame.grid(column=0, row=5, sticky="ew")
        self.content.grid(column=0, row=0, sticky=(S,E,W))
    
        #Putting text into the content frame
        self.welcome_label.grid(column=0, row=0, columnspan=3, padx=5)
        self.text_label.grid(column=0, row=3, columnspan=3, pady=5, padx=5)
    
        #Placing all of the buttons on the menu
        self.yes_button.grid(column=0, row=2)
        self.no_button.grid(column=5, row=2)
        self.separator.grid(column=0, columnspan=6, row=0,sticky=E+W)
    
        # Configuring the expansion of columns and rows if the window size is increased (maximized)
        #parent.columnconfigure(1, weight=1) #Here parent = root
        parent.columnconfigure(0, weight=3)
        parent.columnconfigure(2, weight=3)
        parent.columnconfigure(3, weight=3)
        parent.columnconfigure(4, weight=3)
        parent.rowconfigure(0, weight=3)
        parent.rowconfigure(1, weight=3)
        parent.rowconfigure(2, weight=3)
        parent.rowconfigure(3, weight=3)
        parent.rowconfigure(4, weight=3)
        #parent.rowconfigure(5, weight=1)
  
        self.content.columnconfigure(0, weight=1)
        self.content.columnconfigure(1, weight=1)
        self.content.columnconfigure(2, weight=1)
        self.content.columnconfigure(3, weight=1)
        self.content.columnconfigure(4, weight=1)
        self.content.columnconfigure(5, weight=1)
        self.content.rowconfigure(2, weight=1)


        #self.command_frame.columnconfigure(0, weight = 1)
        self.command_frame.columnconfigure(1, weight = 3)
        self.command_frame.columnconfigure(2, weight = 3)
        self.command_frame.columnconfigure(3, weight = 3)
        self.command_frame.columnconfigure(4, weight = 3)
        self.command_frame.rowconfigure(0, weight=1)
        self.command_frame.rowconfigure(1, weight=1)
        self.command_frame.rowconfigure(2, weight=1)
        self.command_frame.rowconfigure(3, weight=1)
        self.command_frame.rowconfigure(4, weight=1)
        self.command_frame.rowconfigure(5, weight=1)

        return

    def proceed_update(self, event=None):
        """Changing the content frame (not content_frame!) to prepare to update the system.
        The username is automatically grabbed through "whoami" and then it is used within the script here.
        The entire app itself is passed in, which allows us to modify it, which this method will create new content
        to replace the old content which was previously on the screen. """
        
        # Check if root, if so, print an alert and move on, and ask to move on. Possibly a new function
        if self.user.name == "root":
            # Make a text label stating that the user is root, but update anyway.
            pass
        
        # Creating new content for content_frame!
        user_frame = ttk.Frame(self.content_frame)
        if self.user.name != "root":    
            user_label = ttk.Label(user_frame, text = "User: {0}".format(self.user.name), anchor=N)
            sudo_label = ttk.Label(user_frame, text = "Please enter the super-user (sudo) password:".center(66,' '), anchor=CENTER)    
            self.sudo_pass = StringVar()
            sudo_entry = Entry(user_frame, textvariable=self.sudo_pass, show='*', width=25)
            
            user_label.grid(column=0, columnspan=5, row=0, sticky=N)
            separator = ttk.Separator(user_frame, orient=HORIZONTAL)
            separator.grid(column=0, row=1, columnspan=5, sticky=E+W)
            sudo_label.grid(column = 0, columnspan=5, row=2, sticky=(E,W))
            sudo_entry.grid(column=0, columnspan=5, row=3, sticky=(E,W))
        
        elif self.user.name == "root":
            # Here is where need to put warning that you are root and go to new function that doesn't need a password entry
            # Then, the proceed button should take to different function that doesn't need to grab the sudo password and go ahead
            # and update it with the progress bar etc.
            pass
            

        
        # Configuring row/column expansion
        user_frame.columnconfigure(0, weight=1)
        user_frame.columnconfigure(1, weight=1)
        user_frame.columnconfigure(2, weight=1)
        user_frame.columnconfigure(3, weight=1)
        user_frame.columnconfigure(4, weight=1)
        user_frame.columnconfigure(5, weight=1)
        user_frame.rowconfigure(0, weight=1)
        user_frame.rowconfigure(1, weight=1)
        user_frame.rowconfigure(2, weight=1)
        
        # Overwriting previous content, and drawing it to the screen. Effectively destroys what was there previously!
        self.content.destroy()
        self.content = user_frame
        self.yes_button.destroy()
        #Simply overwriting Yes button to avoid having a bunch of random buttons in memory
        self.yes_button = ttk.Button(self.command_frame, text = "Submit")
        self.yes_button.bind("<Button-1>", self.start_update)
        self.yes_button.grid(column=0, row=2)
        self.content.grid(column=0, row=0, sticky=(S,E,W))
        return
    #^----------------------------------------------------- proceed_update(self, event=none)
    
    def start_update(self, event=None):
        """ Function that grabs the sudo password entered into the available entry field.
        Once this password is obtained, it will use it to spawn the process to update the system.
        Also calls the function which will display what is availabe to update."""
        
        
        entry = self.sudo_pass.get()
        self.currentSystem.updateRepos(self.currentSystem.system, entry)
        
        updateChoices = {'rhel':self.currentSystem.get_rhel_updates(), 'arch':'Not impl yet', 'debian':self.currentSystem.get_debian_updates(),\
                         'solus':'Viewing updatabled packages is not available in Solus!'}
        error = 'Error'
        
        
        availUpdates = updateChoices.get(self.currentSystem.system, error)
        if availUpdates == error:
            print('Error in getting update choices')
            print('Perhaps your operating system or Linux distribution is unsupported. See\nREADME.md for more details.')
            sys.exit(5)
        elif availUpdates == '':
            availUpdates = 'System is up to date.'
        # Here during testing
        elif availUpdates == 'Not impl yet':
            # Don't want to do anything yet if the function isn't created!
            # This will need to be taken out when everything is done!
            availUpdates = 'Your system is not supported...yet!!'
            
        
        updateFrame = ttk.Frame(self.content_frame)

        user_label = ttk.Label(updateFrame, text = "Packages available for updating:".center(68,' '), anchor=N)
        availLabel = ttk.Label(updateFrame, text = availUpdates, anchor=CENTER)
        # Making this a stringvar so it can be changed once the update is complete to signify that
        self.completedSwitch = StringVar()
        self.completedSwitch.set('\n\nWould you like to proceed with an update?')
        completeLabel = ttk.Label(updateFrame, textvariable = self.completedSwitch, anchor=CENTER)

        # Recreating another screen to show, will replace self.content
        user_label.grid(column=0, columnspan=5, row=0, sticky=N)
        separator = ttk.Separator(updateFrame, orient=HORIZONTAL)
        separator.grid(column=0, row=1, columnspan=5, sticky=E+W)
        availLabel.grid(column = 0, columnspan=5, row=2, sticky=(E,W))
        completeLabel.grid(column = 0, columnspan=5, row=3, sticky=(E,W))
        
        # Replacing the content frame with the one just created above ^
        self.content.destroy()
        self.content = updateFrame
        self.content.grid(column=0, row=0, sticky=(S,E,W))
        
        # Changing appearance and use of the Yes button, which is on bottom left of screen.
        self.yes_button = ttk.Button(self.command_frame, text = "Proceed")
        self.yes_button.bind("<Button-1>", self.update)
        self.yes_button.grid(column=0, row=2)
    #^----------------------------------------------------- start_update(self, event=None)
    
    def update(self, event=None):
        """Function to actually begin the updating process. Will display to the user that it is
        updating the system and to not close the window. Then it will spawn a process to update the
        system dependent on what type the system is."""
        
        # Entry is the root password
        entry = self.sudo_pass.get()
        
        updateFrame = ttk.Frame(self.content_frame)
        self.user_string = StringVar()
        self.user_string.set("User: {0}".format(self.user.name).center(68,' '))
        
        user_label = ttk.Label(updateFrame, textvariable = self.user_string, anchor=N)
        # Making this a stringvar so it can be changed once the update is complete to signify that
        self.completedSwitch.set('Update in progress. . .'.center(68,' ') + '\n' + \
                                 'Please do not close this window. . .'.center(68,' '))
        completeLabel = ttk.Label(updateFrame, textvariable = self.completedSwitch, anchor=CENTER)

        # Recreating another screen to show, will replace self.content
        user_label.grid(column=0, columnspan=5, row=0, sticky=N)
        separator = ttk.Separator(updateFrame, orient=HORIZONTAL)
        separator.grid(column=0, row=1, columnspan=5, sticky=E+W)
        completeLabel.grid(column = 0, columnspan=5, row=3, sticky=(E,W))
        
        # Replacing the content frame with the one just created above ^
        self.content.destroy()
        self.content = updateFrame
        self.content.grid(column=0, row=0, sticky=(S,E,W))
        
        # Changing appearance and use of the Yes button, which is on bottom left of screen.
        self.yes_button = ttk.Button(self.command_frame, text = "Proceed", state='disabled')
        self.yes_button.bind("<Button-1>", None)
        self.no_button['state'] = 'disabled'
        self.no_button.bind("<Button-1>", None)
        self.yes_button.grid(column=0, row=2)
    
        # Run through and check each possibility for the available distro's
        if self.currentSystem.system == 'solus':
            proc = self.currentSystem.updateSolus(entry)
        elif self.currentSystem.system == 'rhel':
            proc = self.currentSystem.updateRhel(entry)
        elif self.currentSystem.system == 'debian':
            proc = self.currentSystem.updateDebian(entry)
        elif self.currentSystem.system == 'arch':
            # Need to implement
            pass
        else:
            print('Error with current system type.')
            sys.exit(6)
        self.my_parent.update()
        self.wait_patiently(proc)
        self.completedSwitch.set('Update complete!!\n'.center(68,' ') + '\n' + \
                                 'Click Show Info to see information on your system.'.center(68,' ') + '\n' + 'Or click Exit to close the program'.center(68,' '))
        # Saving this into the updates for futrure reading
        self.currentSystem.save_update(self.user.name)
        self.yes_button['state'] = 'enabled'
        self.yes_button['text'] = 'Show Info'
        self.yes_button.bind("<Button-1>", self.show_info)
        self.no_button['state'] = 'enabled'
        self.no_button.bind("<Button-1>", self.endLife)
        self.no_button['text'] = 'Exit'
        self.my_parent.update()
        return
    #^-----------------------------------------------------update(self, event=None)
    
    def show_info(self, event=None):
        """Function to show the user some info on their system. Info is found in Csys class.
        Function will put the new content into a StringVar and refresh the screen."""
        
        if self.user_string.get() == 'Empty':
            updateFrame = ttk.Frame(self.content_frame)
        
            user_label = ttk.Label(updateFrame, textvariable = self.user_string, anchor=N)
            # Making this a stringvar so it can be changed once the update is complete to signify that
            completeLabel = ttk.Label(updateFrame, textvariable = self.completedSwitch, anchor=CENTER)

            # Recreating another screen to show, will replace self.content
            user_label.grid(column=0, columnspan=5, row=0, sticky=N)
            separator = ttk.Separator(updateFrame, orient=HORIZONTAL)
            separator.grid(column=0, row=1, columnspan=5, sticky=E+W)
            completeLabel.grid(column = 0, columnspan=5, row=3, sticky=(E,W))
        
            # Replacing the content frame with the one just created above ^
            self.content.destroy()
            self.content = updateFrame
            self.content.grid(column=0, row=0, sticky=(S,E,W))
            self.no_button.bind("<Button-1>", self.endLife)
            self.no_button['text'] = 'Exit'
            self.my_parent.update()
        
        
        self.user_string.set('Showing System Information')
        format_str = (('CPU: {0}'.format(self.currentSystem.cpu_name).ljust(68,' ')) + '\n'+ \
                                 ('Total Cores: {0}'.format(self.currentSystem.cores).ljust(68,' '))+ '\n' \
                                + ('Total Memory: {0}'.format(self.currentSystem.total_mem).ljust(68,' '))+ '\n' \
                                + ('Used Memory: {0}'.format(self.currentSystem.used_mem).ljust(68,' '))+ '\n'+ \
                                 ('Cached Memory: {0}'.format(self.currentSystem.cached_mem).ljust(68,' '))+ '\n'+ \
                                 ('Free Memory: {0}'.format(self.currentSystem.free_mem).ljust(68,' ')) )
        self.completedSwitch.set(format_str)
        self.yes_button['state'] = 'disabled'
        self.yes_button['text'] = 'Show Info'
        self.yes_button.bind("<Button-1>", self.doNothing)
        self.my_parent.update()
        return

    def doNothing(self, event=None):
        """Function to do absolutely nothing. Used to map hte buttons of tkinter to nothing."""
        return
        
    def endLife(self, event=None):
        """Function to end the root loop of tkinter to essentially server as the binding
        of the exit buttons."""
        self.my_parent.destroy()
        sys.exit()
        
    def wait_patiently(self, proc, event=None):
        """Function to help the timing of the GUI by forcing it to wait in
        another function while the update is taking place."""
        proc.wait()
        time.sleep(.5)
        return
    #^----------------------------------------------------- wait_patiently(self, proc, event=None)  
#^------------------------------------------------------------------------------------------------- Class App_Window

class Csys():
    """Class to represent the objet of Current Sysem (Csys). Contains information such as:
    total_mem, used_mem,free_mem,cached_mem, system_type, last_update."""
    # Current system information, at initialization get all info for use in App_window
    def __init__(self):
        """Instantiation for the current system the script is running on."""
        self.system = self.get_system_type()
        cpu_proc = subprocess.getoutput("lscpu | grep 'Model name:'")
        self.cpu_name = " ".join((cpu_proc.split()[2:]))
        cores_proc = subprocess.getoutput("lscpu | grep 'CPU(s):'")
        self.cores = cores_proc.split()[1]
        self.arch = subprocess.getoutput("uname -m")
        
        mem_free_proc = subprocess.getoutput("free -h")
        temp = mem_free_proc.split()
        self.total_mem = temp[7]
        self.used_mem = temp[8]
        self.free_mem = str(temp[9])
        self.cached_mem = temp[11]
    #^----------------------------------------------------- __init__(self)    
    
    def get_system_type(self):
        """Method to discover what distro the system is, i.e. if system is Debian, Red Hat, Arch
        etc. Will look for the ID in /etc/os-release. This means it will discover Antergos, Manjaro
        and others as Arch, and Xubuntu, Ubuntu, and others as Debian, and Scientific, CentOs, Fedora
        and others  as Red Hat. Method returns the base system as a string."""
        
        
        system_id = (subprocess.getoutput("cat /etc/os-release | grep 'ID='")).split('\n')[0]
        system_id = system_id.replace('"','') # Some systems produce (")'s  others do not!
        system_id = system_id[system_id.find('=') + 1:]
        
        # switch statement wanna-be
        distro_choices = {'fedora': 'rhel', 'centos': 'rhel', 'scientific': 'rhel', 'redhat': 'rhel', \
                          'debian': 'debian', 'ubuntu': 'debian', 'xubuntu': 'debian', 'galliumos': 'debian', \
                          'arch': 'arch', 'antergos': 'arch', 'manjaro': 'arch', 'solus':'solus'}
        default = 'Unknown'
        system = distro_choices.get(system_id, default)
        if system == default:
            # Last ditch effort trying to get correct usage
            system_id = subprocess.getoutput("cat /etc/os-release | grep'ID_LIKE=").split('\n')[0]
            system_id = system_id.replace('"', '')
            
        return system
    #^----------------------------------------------------- find_system_type(self)
    
    def get_last_update(self, user_name):
        """Method to obtain previous update, path is specified as update_file.
        If the file is not found, assuming this is the first time running the script.
        The file will then be created if 'y' is chosen (executing the update)."""
        # Update-file will contain the date/time of the last update. It is hidden hence the prefix '.'
        update_file = ("/home/" + user_name + "/.previous-update.txt")
        try:
            file_ob = open(update_file, 'r')
            last_update = file_ob.readline()
            file_ob.close()
        except FileNotFoundError:
            last_update = "This is the first update!"
        return last_update.rstrip()
    #^----------------------------------------------------- get_last_update(self, user_name)
    
    def save_update(self, user_name):
        """If the system is updated, the time and date will be saved to a file, able to be viewed again"""
        update_file = ("/home/" + user_name + "/.previous-update.txt")
        file_ob = open(update_file, 'w')
        date = subprocess.getoutput('date')
        file_ob.write(str(date))
        file_ob.close()
        return
    #^----------------------------------------------------- save_update(self, user_name)
    
    def updateRepos(self, system, entry):
        """Function to update the repositories of the current system if it is a system that supports
        that. I.e. Arch based systems don't need to update the repositoires, as its automagically done elsewhere."""
        echo = subprocess.Popen(('echo', entry), stdout=subprocess.PIPE)

        if system == 'debian':
            proc = subprocess.Popen(('sudo', '-S', 'apt-get', 'update'), stdin=echo.stdout)
        #process = repo_choices.get(self.system, default)
        elif system == 'arch':
            # Need to add a process similiar to above
            pass
        elif system == 'rhel':
            #proc = subprocess.Popen(('su', '-C', 'yum', 'update'), stdin=echo.stdout)
            pass
        elif system == 'solus':
            proc = subprocess.Popen(('sudo', '-S', 'eopkg', 'ur'), stdin=echo.stdout)
        return
    #^----------------------------------------------------- updateRepos(self, system, entry)
    
    def get_rhel_updates(self):
        """Function to obtain what packages are available for updating from the yum
        package manager."""
        
        yum_list = subprocess.getoutput("yum list updates").split('\n')
        yum_list = yum_list[7:]
        update_list = []
        for package in yum_list:
            update_list.append(package.split()[0])
        return '\n'.join(update_list)
    
    def get_debian_updates(self):
        """Function to obtain what packages are available to update on debian based systems.
        Returns a large formatted string containing what packages can be updated."""
        
        apt_list = subprocess.getoutput("apt list --upgradeable").replace(',','')
        
        apt_list = apt_list[apt_list.find('Listing...') + 10 :]
        apt_list=apt_list.split()
        for item in apt_list:
            item = item[:item.find('/')]
        return apt_list[0]
    #^----------------------------------------------------- get_debian_updates(self)
    
    def updateSolus(self, entry):
        """Function to update a solus system using the eopkg package manager. This PM does
        not allow seeing the available updates before updating, so to find out what needs to be updated
        it must be run all the way through!
        Function will spawn a subprocess for updating Solus, and return the process itself."""
        echo = subprocess.Popen(('echo', entry), stdout=subprocess.PIPE)
        
        update = subprocess.Popen(('sudo', '-S', 'eopkg', '-y', 'up'), stdin=echo.stdout)
        return update
    #^----------------------------------------------------- updateSolus(self, entry)
    
    def updateDebian(self, entry):
        """Function to update a debian system. Starts the process for apt get to update the packages.
        Function returns the process itself (object of subprocess module)"""
        echo = subprocess.Popen(('echo', entry), stdout=subprocess.PIPE)
        
        update = subprocess.Popen(('sudo', '-S', 'apt-get', '-y', 'dist-upgrade'), stdin=echo.stdout)
        return update
    
    def updateRhel(self, entry):
        """Function to start the process of updating a rhel based system with yum as the package
        manager."""
        
        echo = subprocess.Popen(('echo', entry), stdout=subprocess.PIPE)
        
        update = subprocess.Popen(('sudo', '-S', 'yum', '-y', 'update'), stdin=echo.stdout)
        return update
    
#^------------------------------------------------------------------------------------------------- Class Csys

class Suser():
    """Class to hold the information pertaining to the user of the current system. """
    
    def __init__(self):
        env = subprocess.getoutput("env")
        self.parse_env(env)
        return
    
    def parse_env(self, env):
        """Class Function to parse the environment variables of the current user. This will parse out the
        User-name, check if its root, get the PWD, and information to be used later in the GUI. """
        
        env_list = env.split('\n')
        
        # Searching each line that is in env for specific entries (User, pwd, session, DE)
        for line in env_list:
            if 'USER=' in line:
                self.name = line[(line.find('=') + 1) : ]
            #continue searching for important env vars
            
            
        return
        
    
def main():
    """Temporary, need to fill in something here"""
    
    root = Tk()
    root.title("Sys-Update")
    # Now, app is the whole sha-bang! it is a container for the root-window.
    app = App_Window(root)
    #root.resizable(width=False, height=False)
    root.geometry('{}x{}'.format(400, 150))
    root.mainloop()

#^--------------------------------------------------------- main()


# Standard boilerplate to call the main() function.
if __name__ == '__main__':
  main()
