##### all:

```
conan remote add myconan http://172.27.128.202:38081/artifactory/api/conan/conan

conan upload mqttc/1.3.9 --all -r myconan
```

##### windows:

```
conan create . -s compiler="Visual Studio" -s compiler.version=15 -o shared=True
```
