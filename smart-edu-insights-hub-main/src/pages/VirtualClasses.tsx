
import { useEffect, useState } from "react";
import { format, addHours } from "date-fns";
import { Video, Users, CalendarClock, Hourglass, CheckCircle2 } from "lucide-react";
import AppLayout from "@/components/Layout/AppLayout";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { AspectRatio } from "@/components/ui/aspect-ratio";

interface VirtualClass {
  id: number;
  title: string;
  course: string;
  instructor: string;
  startTime: Date;
  duration: number; // in minutes
  status: "upcoming" | "live" | "completed" | "canceled";
  description: string;
  participants?: number;
  recordingUrl?: string;
  thumbnailUrl?: string;
}

const VirtualClasses = () => {
  const [userData, setUserData] = useState<any>(null);
  const [activeTab, setActiveTab] = useState("all");
  const [currentTime] = useState(new Date());
  
  useEffect(() => {
    // Get user data from localStorage
    const userDataString = localStorage.getItem("lms-user");
    if (userDataString) {
      const parsedUserData = JSON.parse(userDataString);
      setUserData(parsedUserData);
    }
  }, []);
  
  // Sample virtual classes data
  const commonClasses: VirtualClass[] = [
    {
      id: 1,
      title: "JavaScript Event Loop Deep Dive",
      course: "Introduction to Programming",
      instructor: "Dr. Sarah Johnson",
      startTime: addHours(new Date(), 1),
      duration: 60,
      status: "upcoming",
      description: "Detailed explanation of JavaScript's event loop and asynchronous programming.",
      participants: 38,
      thumbnailUrl: "https://images.unsplash.com/photo-1487058792275-0ad4aaf24ca7?auto=format&fit=crop&w=1470&q=80"
    },
    {
      id: 2,
      title: "AVL Trees and Self-Balancing Trees",
      course: "Data Structures and Algorithms",
      instructor: "Prof. Michael Chen",
      startTime: new Date(),
      duration: 90,
      status: "live",
      description: "Understanding self-balancing binary search trees and their implementations.",
      participants: 42,
      thumbnailUrl: "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1470&q=80"
    },
    {
      id: 3,
      title: "SQL Query Optimization",
      course: "Database Management Systems",
      instructor: "Dr. David Wilson",
      startTime: new Date(currentTime.getTime() - 7200000), // 2 hours ago
      duration: 75,
      status: "completed",
      description: "Learn advanced techniques for optimizing SQL queries for performance.",
      participants: 35,
      recordingUrl: "https://example.com/recording/123",
      thumbnailUrl: "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?auto=format&fit=crop&w=1470&q=80"
    },
    {
      id: 4,
      title: "Neural Networks and Deep Learning",
      course: "Artificial Intelligence Basics",
      instructor: "Prof. Emily Rodriguez",
      startTime: addHours(new Date(), 26),
      duration: 120,
      status: "upcoming",
      description: "Introduction to neural network architectures and deep learning concepts.",
      participants: 0,
      thumbnailUrl: "https://images.unsplash.com/photo-1581090464777-f3220bbe1b8b?auto=format&fit=crop&w=1470&q=80"
    },
    {
      id: 5,
      title: "Advanced React Patterns",
      course: "Web Development",
      instructor: userData?.userType === "faculty" ? "You" : "Prof. Alex Morgan",
      startTime: new Date(currentTime.getTime() - 259200000), // 3 days ago
      duration: 90,
      status: "completed",
      description: "Exploring advanced React design patterns and best practices.",
      participants: 32,
      recordingUrl: "https://example.com/recording/456",
      thumbnailUrl: "https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?auto=format&fit=crop&w=1470&q=80"
    }
  ];
  
  const classes = commonClasses.map(cls => {
    if (userData?.userType === "faculty" && cls.instructor === "You") {
      return {...cls, participants: 32};
    }
    return cls;
  });
  
  const filteredClasses = activeTab === "all" 
    ? classes 
    : classes.filter(cls => cls.status === activeTab);
  
  const getStatusBadge = (status: string) => {
    switch(status) {
      case "upcoming":
        return <Badge variant="outline">Upcoming</Badge>;
      case "live":
        return <Badge variant="destructive" className="bg-red-500 hover:bg-red-600 animate-pulse">Live Now</Badge>;
      case "completed":
        return <Badge variant="secondary">Completed</Badge>;
      case "canceled":
        return <Badge variant="destructive">Canceled</Badge>;
      default:
        return <Badge variant="outline">{status}</Badge>;
    }
  };
  
  const formatDuration = (minutes: number) => {
    if (minutes < 60) return `${minutes} min`;
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return `${hours}h${mins > 0 ? ` ${mins}m` : ''}`;
  };
  
  if (!userData) {
    return <div>Loading...</div>;
  }
  
  return (
    <AppLayout>
      <div className="max-w-7xl mx-auto">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-800">Virtual Classes</h1>
          <p className="text-gray-600">
            {userData.userType === "student" 
              ? "Join live classes and access recordings." 
              : "Manage your virtual classroom sessions."}
          </p>
        </div>
        
        <Tabs defaultValue="all" className="mb-8" onValueChange={setActiveTab}>
          <TabsList>
            <TabsTrigger value="all">All Classes</TabsTrigger>
            <TabsTrigger value="live">Live Now</TabsTrigger>
            <TabsTrigger value="upcoming">Upcoming</TabsTrigger>
            <TabsTrigger value="completed">Completed</TabsTrigger>
          </TabsList>
          
          <TabsContent value={activeTab} className="mt-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredClasses.map((virtualClass) => (
                <Card key={virtualClass.id} className="overflow-hidden">
                  <AspectRatio ratio={16 / 9} className="bg-muted">
                    {virtualClass.thumbnailUrl ? (
                      <img 
                        src={virtualClass.thumbnailUrl} 
                        alt={virtualClass.title}
                        className="object-cover w-full h-full"
                      />
                    ) : (
                      <div className="flex items-center justify-center w-full h-full bg-gray-200">
                        <Video className="h-12 w-12 text-gray-400" />
                      </div>
                    )}
                    {virtualClass.status === "live" && (
                      <div className="absolute top-2 right-2">
                        <Badge variant="destructive" className="bg-red-500 hover:bg-red-600 animate-pulse">
                          LIVE
                        </Badge>
                      </div>
                    )}
                  </AspectRatio>
                  <CardHeader className="pb-2">
                    <div className="flex justify-between items-start">
                      <CardDescription>{virtualClass.course}</CardDescription>
                      {getStatusBadge(virtualClass.status)}
                    </div>
                    <CardTitle className="text-lg line-clamp-1">{virtualClass.title}</CardTitle>
                    <CardDescription className="line-clamp-2">
                      {virtualClass.description}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="pb-2">
                    <div className="grid grid-cols-2 gap-2 text-sm">
                      <div className="flex items-center text-muted-foreground">
                        <Users className="h-4 w-4 mr-1" />
                        <span>
                          {virtualClass.status === "upcoming" && userData.userType !== "faculty" 
                            ? "Not started" 
                            : `${virtualClass.participants} ${userData.userType === "faculty" ? "Students" : "Participants"}`}
                        </span>
                      </div>
                      <div className="flex items-center text-muted-foreground">
                        <Hourglass className="h-4 w-4 mr-1" />
                        <span>{formatDuration(virtualClass.duration)}</span>
                      </div>
                      <div className="flex items-center text-muted-foreground col-span-2">
                        <CalendarClock className="h-4 w-4 mr-1" />
                        <span>
                          {format(virtualClass.startTime, "MMM d, yyyy • h:mm a")}
                        </span>
                      </div>
                    </div>
                  </CardContent>
                  <CardFooter>
                    {virtualClass.status === "live" ? (
                      <Button variant="destructive" className="w-full">
                        Join Live Class
                      </Button>
                    ) : virtualClass.status === "completed" ? (
                      <Button variant="outline" className="w-full">
                        <CheckCircle2 className="mr-2 h-4 w-4" />
                        Watch Recording
                      </Button>
                    ) : (
                      <Button 
                        variant="default" 
                        className="w-full"
                        disabled={userData.userType === "student"}
                      >
                        {userData.userType === "faculty" ? "Start Class" : "Waiting to Start"}
                      </Button>
                    )}
                  </CardFooter>
                </Card>
              ))}
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </AppLayout>
  );
};

export default VirtualClasses;
