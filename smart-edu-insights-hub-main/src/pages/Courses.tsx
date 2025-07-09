
import AppLayout from "@/components/Layout/AppLayout";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { BookOpen, ChevronRight, Clock, Users } from "lucide-react";
import { useEffect, useState } from "react";

interface Course {
  id: number;
  title: string;
  description: string;
  instructor: string;
  progress?: number;
  students?: number;
  startDate: string;
  category: string;
}

const Courses = () => {
  const [userData, setUserData] = useState<any>(null);
  const [courses, setCourses] = useState<Course[]>([]);

  useEffect(() => {
    // Get user data from localStorage
    const userDataString = localStorage.getItem("lms-user");
    if (userDataString) {
      const parsedUserData = JSON.parse(userDataString);
      setUserData(parsedUserData);

      // Set courses based on user type
      if (parsedUserData.userType === "faculty") {
        setCourses(facultyCourses);
      } else {
        setCourses(studentCourses);
      }
    }
  }, []);

  // Sample data for courses
  const studentCourses: Course[] = [
    { 
      id: 1, 
      title: "Introduction to Programming", 
      description: "Learn the fundamentals of programming with JavaScript.",
      instructor: "Dr. Sarah Johnson", 
      progress: 75, 
      startDate: "Jan 15, 2025",
      category: "Computer Science"
    },
    { 
      id: 2, 
      title: "Data Structures and Algorithms", 
      description: "Master common data structures and algorithm design principles.",
      instructor: "Prof. Michael Chen", 
      progress: 60, 
      startDate: "Feb 1, 2025",
      category: "Computer Science" 
    },
    { 
      id: 3, 
      title: "Database Management Systems", 
      description: "Fundamentals of relational databases and SQL.",
      instructor: "Dr. David Wilson", 
      progress: 90,
      startDate: "Jan 10, 2025",
      category: "Information Technology"
    },
    { 
      id: 4, 
      title: "Artificial Intelligence Basics", 
      description: "Introduction to AI concepts and applications.",
      instructor: "Prof. Emily Rodriguez", 
      progress: 30,
      startDate: "Feb 20, 2025",
      category: "Computer Science"
    }
  ];

  const facultyCourses: Course[] = [
    { 
      id: 1, 
      title: "Advanced Programming", 
      description: "Object-oriented and functional programming paradigms.",
      instructor: "You", 
      progress: 80, 
      students: 45,
      startDate: "Jan 5, 2025",
      category: "Computer Science"
    },
    { 
      id: 2, 
      title: "Web Development", 
      description: "Modern web application development with React.",
      instructor: "You", 
      progress: 60, 
      students: 38,
      startDate: "Jan 22, 2025",
      category: "Information Technology"
    },
    { 
      id: 3, 
      title: "Mobile App Development", 
      description: "Cross-platform mobile app development techniques.",
      instructor: "You", 
      progress: 40, 
      students: 32,
      startDate: "Feb 10, 2025",
      category: "Computer Science"
    }
  ];

  const courseCategories = Array.from(new Set(courses.map(course => course.category)));

  if (!userData) {
    return <div>Loading...</div>;
  }

  return (
    <AppLayout>
      <div className="max-w-7xl mx-auto">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-800">
            {userData.userType === "student" ? "My Courses" : "Courses You Teach"}
          </h1>
          <p className="text-gray-600">
            {userData.userType === "student" 
              ? "Access your enrolled courses and track your progress." 
              : "Manage and organize the courses you're teaching."}
          </p>
        </div>

        {courseCategories.map(category => (
          <div key={category} className="mb-8">
            <h2 className="text-xl font-semibold mb-4">{category}</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {courses
                .filter(course => course.category === category)
                .map(course => (
                  <Card key={course.id} className="overflow-hidden hover:shadow-lg transition-shadow">
                    <CardHeader className="pb-3">
                      <div className="flex justify-between items-start">
                        <Badge variant="outline" className="mb-2">
                          {course.category}
                        </Badge>
                        <Badge variant={course.progress && course.progress > 70 ? "default" : "secondary"}>
                          {course.progress ? `${course.progress}% Complete` : "Not Started"}
                        </Badge>
                      </div>
                      <CardTitle className="text-lg">{course.title}</CardTitle>
                      <CardDescription>{course.description}</CardDescription>
                    </CardHeader>
                    <CardContent className="pb-3">
                      <div className="space-y-2">
                        <div className="flex items-center justify-between text-sm">
                          <div className="flex items-center">
                            <BookOpen className="h-4 w-4 mr-1 text-muted-foreground" />
                            <span>
                              {userData.userType === "student" 
                                ? `Instructor: ${course.instructor}` 
                                : `${course.students} Students`}
                            </span>
                          </div>
                          <div className="flex items-center">
                            <Clock className="h-4 w-4 mr-1 text-muted-foreground" />
                            <span>Started {course.startDate}</span>
                          </div>
                        </div>
                        {course.progress !== undefined && (
                          <Progress value={course.progress} className="h-2" />
                        )}
                      </div>
                    </CardContent>
                    <CardFooter>
                      <Button variant="outline" className="w-full">
                        <span>Open Course</span>
                        <ChevronRight className="h-4 w-4 ml-1" />
                      </Button>
                    </CardFooter>
                  </Card>
                ))}
            </div>
          </div>
        ))}
      </div>
    </AppLayout>
  );
};

export default Courses;
