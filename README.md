##### all:

```
conan remote add myconan http://172.27.128.202:38081/artifactory/api/conan/conan
```

##### windows:

```
conan create . -s compiler="Visual Studio" -s compiler.version=15
```
