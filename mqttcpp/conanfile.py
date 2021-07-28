from conans import ConanFile, CMake, tools


class MqttcppConan(ConanFile):
    name = "mqttcpp"
    version = "1.2.0"
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Mqttcpp here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "cmake"
    requires = [("mqttc/1.3.9")]

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        self.run(
            "git clone https://github.com/eclipse/paho.mqtt.cpp.git -b v%s" % (self.version))
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("paho.mqtt.cpp/CMakeLists.txt",
                              "## --- Build options ---",
                              '''include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

## --- Build options ---''')

    def build(self):
        cmake = CMake(self)
        cmake.definitions["PAHO_WITH_SSL"] = "FALSE"
        if self.options.shared:
            cmake.definitions["PAHO_BUILD_SHARED"] = "TRUE"
            cmake.definitions["PAHO_BUILD_STATIC"] = "FALSE"
        else:
            cmake.definitions["PAHO_BUILD_SHARED"] = "FALSE"
            cmake.definitions["PAHO_BUILD_STATIC"] = "TRUE"
        cmake.configure(source_folder="paho.mqtt.cpp")
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="paho.mqtt.cpp/src")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["paho-mqttpp3"]
