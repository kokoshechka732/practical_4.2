#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <deque>
#include <string>
#include <sstream>
#include <cstring>

namespace py = pybind11;

struct Elem {
    int num;
    char txt[10];
};

class DequeSTL {
private:
    std::deque<Elem> d;

public:
    void push_front(int n, const std::string& t) {
        Elem e;
        e.num = n;
        std::strncpy(e.txt, t.c_str(), 9);
        e.txt[9] = '\0';
        d.push_front(e);
    }

    void push_back(int n, const std::string& t) {
        Elem e;
        e.num = n;
        std::strncpy(e.txt, t.c_str(), 9);
        e.txt[9] = '\0';
        d.push_back(e);
    }

    bool pop_front() {
        if (d.empty()) return false;
        d.pop_front();
        return true;
    }

    bool pop_back() {
        if (d.empty()) return false;
        d.pop_back();
        return true;
    }

    int get_size() {
        return static_cast<int>(d.size());
    }

    bool is_empty() {
        return d.empty();
    }

    std::string to_string() {
        if (d.empty()) return "";
        std::ostringstream oss;
        int i = 0;
        for (const auto& e : d) {
            oss << "[" << i << "] число: " << e.num
                << ", текст: \"" << e.txt << "\"\n";
            i++;
        }
        return oss.str();
    }

    void clear() {
        d.clear();
    }
};

PYBIND11_MODULE(last_deque_stl, m) {
    py::class_<DequeSTL>(m, "DequeSTL")
        .def(py::init<>())
        .def("push_front", &DequeSTL::push_front)
        .def("push_back", &DequeSTL::push_back)
        .def("pop_front", &DequeSTL::pop_front)
        .def("pop_back", &DequeSTL::pop_back)
        .def("get_size", &DequeSTL::get_size)
        .def("is_empty", &DequeSTL::is_empty)
        .def("to_string", &DequeSTL::to_string)
        .def("clear", &DequeSTL::clear);
}