
import { useEffect, useState } from "react";
import AppLayout from "@/components/Layout/AppLayout";
import CourseCard from "@/components/Dashboard/CourseCard";
import UpcomingTasks from "@/components/Dashboard/UpcomingTasks";
import AnalyticsChart from "@/components/Dashboard/AnalyticsChart";

interface UserData {
  email: string;
  userType: string;
  name: string;
  isLoggedIn: boolean;
}

// Sample data for courses
const studentCourses = [
  { id: 1, title: "Introduction to Programming", instructor: "Dr. Sarah Johnson", progress: 75, dueAssignments: 2 },
  { id: 2, title: "Data Structures and Algorithms", instructor: "Prof. Michael Chen", progress: 60, dueAssignments: 1 },
  { id: 3, title: "Database Management Systems", instructor: "Dr. David Wilson", progress: 90 },
  { id: 4, title: "Artificial Intelligence Basics", instructor: "Prof. Emily Rodriguez", progress: 30, dueAssignments: 3 }
];

const facultyCourses = [
  { id: 1, title: "Advanced Programming", instructor: "You", progress: 80, students: 45 },
  { id: 2, title: "Web Development", instructor: "You", progress: 60, students: 38 },
  { id: 3, title: "Mobile App Development", instructor: "You", progress: 40, students: 32 }
];

const Dashboard = () => {
  const [userData, setUserData] = useState<UserData | null>(null);
  const [courses, setCourses] = useState([]);

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
  
  if (!userData) {
    return <div>Loading...</div>;
  }
  
  return (
    <AppLayout>
      <div className="max-w-7xl mx-auto">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-800">
            Welcome back, {userData.name}!
          </h1>
          <p className="text-gray-600">
            {userData.userType === "student" 
              ? "Track your academic progress and stay on top of your assignments." 
              : "Manage your courses and monitor student performance."}
          </p>
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <section className="dashboard-section">
              <h2 className="dashboard-section-title">
                {userData.userType === "student" ? "My Courses" : "Courses You Teach"}
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {courses.map((course: any) => (
                  <CourseCard 
                    key={course.id}
                    title={course.title}
                    instructor={course.instructor}
                    progress={course.progress}
                    dueAssignments={course.dueAssignments}
                  />
                ))}
              </div>
            </section>
            
            <section className="dashboard-section">
              <h2 className="dashboard-section-title">Performance Analytics</h2>
              <div className="dashboard-card">
                <AnalyticsChart />
              </div>
            </section>
          </div>
          
          <div className="space-y-6">
            <section className="dashboard-section">
              <h2 className="dashboard-section-title">What's Next</h2>
              <UpcomingTasks />
            </section>
            
            <section className="dashboard-section">
              <h2 className="dashboard-section-title">Quick Stats</h2>
              <div className="grid grid-cols-2 gap-4">
                <div className="dashboard-card">
                  <div className="text-sm text-gray-500">
                    {userData.userType === "student" ? "Assignments Due" : "Pending Grades"}
                  </div>
                  <div className="text-3xl font-bold mt-1">6</div>
                </div>
                <div className="dashboard-card">
                  <div className="text-sm text-gray-500">
                    {userData.userType === "student" ? "Average Grade" : "Active Courses"}
                  </div>
                  <div className="text-3xl font-bold mt-1">
                    {userData.userType === "student" ? "83%" : "3"}
                  </div>
                </div>
                <div className="dashboard-card">
                  <div className="text-sm text-gray-500">Upcoming Classes</div>
                  <div className="text-3xl font-bold mt-1">2</div>
                </div>
                <div className="dashboard-card">
                  <div className="text-sm text-gray-500">
                    {userData.userType === "student" ? "Attendance" : "Total Students"}
                  </div>
                  <div className="text-3xl font-bold mt-1">
                    {userData.userType === "student" ? "94%" : "115"}
                  </div>
                </div>
              </div>
            </section>
          </div>
        </div>
      </div>
    </AppLayout>
  );
};

export default Dashboard;
