import { useEffect, useState } from "react";
import { format } from "date-fns";
import { FileText, Clock, AlertCircle } from "lucide-react";
import AppLayout from "@/components/Layout/AppLayout";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Progress } from "@/components/ui/progress";

interface Assignment {
  id: number;
  title: string;
  course: string;
  dueDate: Date;
  status: "pending" | "submitted" | "graded" | "late" | "upcoming";
  description: string;
  grade?: number;
  feedback?: string;
  submissionCount?: number;
  totalSubmissions?: number;
}

const Assignments = () => {
  const [userData, setUserData] = useState<any>(null);
  const [activeTab, setActiveTab] = useState("all");
  
  useEffect(() => {
    // Get user data from localStorage
    const userDataString = localStorage.getItem("lms-user");
    if (userDataString) {
      const parsedUserData = JSON.parse(userDataString);
      setUserData(parsedUserData);
    }
  }, []);
  
  // Sample assignment data
  const studentAssignments: Assignment[] = [
    {
      id: 1,
      title: "JavaScript Basics Quiz",
      course: "Introduction to Programming",
      dueDate: new Date("2025-06-01"),
      status: "submitted",
      description: "Complete the online quiz about JavaScript fundamentals."
    },
    {
      id: 2,
      title: "Binary Search Tree Implementation",
      course: "Data Structures and Algorithms",
      dueDate: new Date("2025-05-20"),
      status: "graded",
      description: "Implement a binary search tree with insert, delete, and search operations.",
      grade: 92,
      feedback: "Excellent work! Your implementation is very efficient."
    },
    {
      id: 3,
      title: "Database Schema Design",
      course: "Database Management Systems",
      dueDate: new Date("2025-05-25"),
      status: "pending",
      description: "Design a database schema for an online bookstore."
    },
    {
      id: 4,
      title: "Machine Learning Model Training",
      course: "Artificial Intelligence Basics",
      dueDate: new Date("2025-05-18"),
      status: "late",
      description: "Train a simple classification model using the provided dataset."
    },
    {
      id: 5,
      title: "Neural Network Architecture",
      course: "Artificial Intelligence Basics",
      dueDate: new Date("2025-06-10"),
      status: "upcoming",
      description: "Design a neural network architecture for image recognition."
    }
  ];
  
  const facultyAssignments: Assignment[] = [
    {
      id: 1,
      title: "OOP Design Patterns",
      course: "Advanced Programming",
      dueDate: new Date("2025-05-30"),
      status: "pending",
      description: "Implement three design patterns of your choice and explain their applications.",
      submissionCount: 32,
      totalSubmissions: 45
    },
    {
      id: 2,
      title: "React State Management",
      course: "Web Development",
      dueDate: new Date("2025-05-26"),
      status: "graded",
      description: "Create a React application demonstrating different state management techniques.",
      submissionCount: 38,
      totalSubmissions: 38
    },
    {
      id: 3,
      title: "Cross-platform UI Development",
      course: "Mobile App Development",
      dueDate: new Date("2025-06-05"),
      status: "upcoming",
      description: "Build a simple mobile app UI that works on both iOS and Android.",
      submissionCount: 0,
      totalSubmissions: 32
    }
  ];
  
  const assignments = userData?.userType === "faculty" ? facultyAssignments : studentAssignments;
  
  const filteredAssignments = activeTab === "all" 
    ? assignments 
    : assignments.filter(assignment => assignment.status === activeTab);
  
  const getStatusBadge = (status: string) => {
    switch(status) {
      case "submitted":
        return <Badge variant="secondary">Submitted</Badge>;
      case "graded":
        return <Badge variant="outline" className="bg-green-500 text-white hover:bg-green-600">Graded</Badge>;
      case "pending":
        return <Badge>Pending</Badge>;
      case "late":
        return <Badge variant="destructive">Late</Badge>;
      case "upcoming":
        return <Badge variant="outline">Upcoming</Badge>;
      default:
        return <Badge variant="outline">{status}</Badge>;
    }
  };
  
  if (!userData) {
    return <div>Loading...</div>;
  }
  
  return (
    <AppLayout>
      <div className="max-w-7xl mx-auto">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-800">
            {userData.userType === "student" ? "My Assignments" : "Assignments"}
          </h1>
          <p className="text-gray-600">
            {userData.userType === "student" 
              ? "Track and submit your assignments." 
              : "Manage assignments and grade submissions."}
          </p>
        </div>
        
        <Tabs defaultValue="all" className="mb-8" onValueChange={setActiveTab}>
          <TabsList>
            <TabsTrigger value="all">All</TabsTrigger>
            <TabsTrigger value="pending">Pending</TabsTrigger>
            <TabsTrigger value="submitted">Submitted</TabsTrigger>
            <TabsTrigger value="graded">Graded</TabsTrigger>
            <TabsTrigger value="late">Late</TabsTrigger>
            <TabsTrigger value="upcoming">Upcoming</TabsTrigger>
          </TabsList>
          
          <TabsContent value={activeTab} className="mt-6">
            <div className="space-y-4">
              {filteredAssignments.length > 0 ? (
                filteredAssignments.map((assignment) => (
                  <Card key={assignment.id}>
                    <CardHeader className="pb-3">
                      <div className="flex justify-between items-center">
                        <div>
                          <CardTitle>{assignment.title}</CardTitle>
                          <CardDescription>{assignment.course}</CardDescription>
                        </div>
                        {getStatusBadge(assignment.status)}
                      </div>
                    </CardHeader>
                    <CardContent className="pb-3">
                      <p className="text-sm text-gray-600 mb-4">
                        {assignment.description}
                      </p>
                      
                      <div className="flex items-center justify-between text-sm">
                        <div className="flex items-center text-muted-foreground">
                          <FileText className="h-4 w-4 mr-1" />
                          <span>
                            {userData.userType === "faculty" 
                              ? `${assignment.submissionCount}/${assignment.totalSubmissions} Submissions` 
                              : assignment.status === "graded" ? `Grade: ${assignment.grade}%` : "Assignment"}
                          </span>
                        </div>
                        
                        <div className="flex items-center text-muted-foreground">
                          <Clock className="h-4 w-4 mr-1" />
                          <span>Due {format(assignment.dueDate, "MMM d, yyyy")}</span>
                        </div>
                      </div>
                      
                      {userData.userType === "faculty" && assignment.submissionCount !== undefined && (
                        <Progress 
                          value={(assignment.submissionCount / assignment.totalSubmissions!) * 100} 
                          className="h-2 mt-4" 
                        />
                      )}
                      
                      {userData.userType === "student" && assignment.status === "graded" && assignment.feedback && (
                        <div className="mt-4 p-3 bg-muted rounded-lg text-sm">
                          <div className="font-medium mb-1">Feedback:</div>
                          <p>{assignment.feedback}</p>
                        </div>
                      )}
                    </CardContent>
                    <CardFooter>
                      {userData.userType === "student" ? (
                        <Button 
                          variant={assignment.status === "graded" ? "outline" : "default"} 
                          className="w-full"
                          disabled={assignment.status === "graded"}
                        >
                          {assignment.status === "submitted" ? "View Submission" : 
                           assignment.status === "graded" ? "Graded" : "Submit Assignment"}
                        </Button>
                      ) : (
                        <Button variant="default" className="w-full">
                          {assignment.status === "graded" ? "View Submissions" : "Grade Submissions"}
                        </Button>
                      )}
                    </CardFooter>
                  </Card>
                ))
              ) : (
                <div className="text-center py-12">
                  <AlertCircle className="h-10 w-10 mx-auto text-muted-foreground mb-4" />
                  <h3 className="font-medium text-lg mb-1">No assignments found</h3>
                  <p className="text-muted-foreground">
                    {activeTab === "all" 
                      ? "You don't have any assignments yet." 
                      : `You don't have any ${activeTab} assignments.`}
                  </p>
                </div>
              )}
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </AppLayout>
  );
};

export default Assignments;
