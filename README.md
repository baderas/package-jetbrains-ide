# package-jetbrains-ide
Creates .deb packages for Jetbrains IDEs (e.g. PyCharm, Intelli IDEA) for Debian/Ubuntu

This project is a further development of [pycharm-dpkg](https://github.com/baderas/pycharm-dpkg) and [intellij-idea-dpkg](https://github.com/trygvis/intellij-idea-dpkg).

# Supported IDEs
* IntelliJ IDEA
* PyCharm

# Supported Distributions
* Debian
* Other distributions based on Debian (e.g., Ubuntu)

# Supported Editions
* Community
* Professional

# Synopsis
`./package.py [-h] [-e EDITION] [-i IDE] [-l] [-c] [-v]`

# Options
* `-h, --help`
   Show this help message and exit
* `-e EDITION, --edition EDITION`
   Which edition should be packaged?
* `-i IDE, --ide IDE`
   Which IDE should be packaged?
* `-l, --list`
   List all supported IDEs
* `-c, --check`
   Check if installed version is older than the newest version available (needs dpkg)
* `-v, --version`
   Show program's version number and exit


# Usage
## Build newest version
`python3 package.py -i idea -e community`
## Check if a newer version than installed is available
`python3 package.py -i idea -e community -c`
## Automated check, build and install in a bash script
```bash
for ide in "idea" "pycharm"; do
    folder=$(mktemp -d)
    cp -r /path/to/package-jetbrains-ide $folder/
    if [ $? -ne 0 ]; then
        echo "Error while executing 'cp -r /path/to/package-jetbrains-ide $folder/'."
        exit -1
    fi
    cd $folder
    echo "Checking for available $ide updates..."
    python3 $folder/package-jetbrains-ide/package.py -i $ide -e community -c
    ret=$?
    if [ $ret -eq 1 ]; then
        echo "Upgrade for $ide available, installing..."
        dpkg_cmd=$(python3 $folder/package-jetbrains-ide/package.py -i $ide -e community)
        dpkg_cmd=$(echo "$dpkg_cmd" | grep -o -E "dpkg -i .*\.deb")
        ret=$?
        if [ $ret -eq 0 ]; then
            sudo $dpkg_cmd
            if [ $? -ne 0 ]; then
                echo "An error occurred while installing $ide with $dpkg_cmd"
            fi
        else
            echo "An error occurred while  packaging $ide"
        fi
    elif [ $ret -eq -1 ]; then
        echo "An error occurred while executing $folder/package-jetbrains-ide/package.py"
    fi
    rm -r $folder
done

```

# Contribution / Bugs
Other IDEs can easily be added, just look into data/* and add necessary files accordingly. Add the IDE to `supportedIDEs` in package.py afterward.

If you find a bug, please file a bug on GitHub: http://github.com/package-jetbrains-ide/pycharm-dpkg/issues

If you want to contribute, please add a pull request on GitHub: http://github.com/package-jetbrains-ide/pycharm-dpkg/pulls

# Credits
The project, idea, and many files are based on trygvis's [intellij-idea-dpkg](https://github.com/trygvis/intellij-idea-dpkg).
