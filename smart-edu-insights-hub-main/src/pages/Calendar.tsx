
import { useEffect, useState } from "react";
import { format, addDays } from "date-fns";
import { Calendar as CalendarComponent } from "@/components/ui/calendar";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import AppLayout from "@/components/Layout/AppLayout";
import { BookOpen, FileText, Video, Calendar as CalendarIcon, ChevronLeft, ChevronRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

interface CalendarEvent {
  id: number;
  title: string;
  date: Date;
  type: "class" | "assignment" | "exam" | "other";
  course: string;
  description?: string;
  time?: string;
}

const CalendarPage = () => {
  const [userData, setUserData] = useState<any>(null);
  const [date, setDate] = useState<Date>(new Date());
  const [selectedView, setSelectedView] = useState<string>("day");
  const [events, setEvents] = useState<CalendarEvent[]>([]);

  useEffect(() => {
    // Get user data from localStorage
    const userDataString = localStorage.getItem("lms-user");
    if (userDataString) {
      const parsedUserData = JSON.parse(userDataString);
      setUserData(parsedUserData);
    }

    // Generate sample events
    const today = new Date();
    const sampleEvents: CalendarEvent[] = [
      {
        id: 1,
        title: "JavaScript Event Loop Deep Dive",
        date: addDays(today, 1),
        type: "class",
        course: "Introduction to Programming",
        time: "10:00 AM - 11:00 AM",
        description: "Virtual class on JavaScript's event loop"
      },
      {
        id: 2,
        title: "JavaScript Basics Quiz",
        date: today,
        type: "assignment",
        course: "Introduction to Programming",
        time: "Due by 11:59 PM",
        description: "Online quiz covering JavaScript fundamentals"
      },
      {
        id: 3,
        title: "Database Schema Design",
        date: addDays(today, 2),
        type: "assignment",
        course: "Database Management Systems",
        time: "Due by 11:59 PM",
        description: "Design a database schema for an online bookstore"
      },
      {
        id: 4,
        title: "Neural Networks and Deep Learning",
        date: addDays(today, 3),
        type: "class",
        course: "Artificial Intelligence Basics",
        time: "2:00 PM - 4:00 PM",
        description: "Introduction to neural networks and deep learning concepts"
      },
      {
        id: 5,
        title: "Midterm Exam",
        date: addDays(today, 5),
        type: "exam",
        course: "Data Structures and Algorithms",
        time: "1:00 PM - 3:00 PM",
        description: "Comprehensive exam covering all topics from weeks 1-6"
      },
      {
        id: 6,
        title: "AVL Trees and Self-Balancing Trees",
        date: today,
        type: "class",
        course: "Data Structures and Algorithms",
        time: "3:30 PM - 5:00 PM",
        description: "Understanding self-balancing binary search trees"
      },
      {
        id: 7,
        title: "SQL Query Optimization",
        date: addDays(today, -1),
        type: "class",
        course: "Database Management Systems",
        time: "11:00 AM - 12:15 PM",
        description: "Advanced techniques for optimizing SQL queries"
      }
    ];
    
    setEvents(sampleEvents);
  }, []);

  const getDayEvents = (day: Date) => {
    return events.filter(event => 
      format(event.date, "yyyy-MM-dd") === format(day, "yyyy-MM-dd")
    );
  };
  
  const todayEvents = getDayEvents(date);
  
  const getEventIcon = (type: string) => {
    switch(type) {
      case "class":
        return <Video className="h-4 w-4" />;
      case "assignment":
        return <FileText className="h-4 w-4" />;
      case "exam":
        return <BookOpen className="h-4 w-4" />;
      default:
        return <CalendarIcon className="h-4 w-4" />;
    }
  };
  
  const getEventBadge = (type: string) => {
    switch(type) {
      case "class":
        return <Badge variant="outline" className="border-blue-500 text-blue-500">Virtual Class</Badge>;
      case "assignment":
        return <Badge variant="outline" className="border-amber-500 text-amber-500">Assignment</Badge>;
      case "exam":
        return <Badge variant="outline" className="border-red-500 text-red-500">Exam</Badge>;
      default:
        return <Badge variant="outline">Event</Badge>;
    }
  };

  if (!userData) {
    return <div>Loading...</div>;
  }

  return (
    <AppLayout>
      <div className="max-w-7xl mx-auto">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-800">Academic Calendar</h1>
          <p className="text-gray-600">
            Track your schedule, assignments, exams, and virtual classes.
          </p>
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-1">
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-lg">Calendar</CardTitle>
                <CardDescription>Select a date to view events</CardDescription>
              </CardHeader>
              <CardContent>
                <CalendarComponent
                  mode="single"
                  selected={date}
                  onSelect={(selectedDate) => selectedDate && setDate(selectedDate)}
                  className="rounded-md border pointer-events-auto"
                  modifiers={{
                    hasEvent: (day) => events.some(
                      event => format(event.date, "yyyy-MM-dd") === format(day, "yyyy-MM-dd")
                    )
                  }}
                  modifiersClassNames={{
                    hasEvent: "bg-primary/10 font-bold text-primary"
                  }}
                />
              </CardContent>
            </Card>
          </div>
          
          <div className="lg:col-span-2">
            <Card>
              <CardHeader className="pb-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Button variant="outline" size="icon" onClick={() => setDate(addDays(date, -1))}>
                      <ChevronLeft className="h-4 w-4" />
                    </Button>
                    <Button variant="outline" onClick={() => setDate(new Date())}>
                      Today
                    </Button>
                    <Button variant="outline" size="icon" onClick={() => setDate(addDays(date, 1))}>
                      <ChevronRight className="h-4 w-4" />
                    </Button>
                  </div>
                  <Select value={selectedView} onValueChange={setSelectedView}>
                    <SelectTrigger className="w-[120px]">
                      <SelectValue placeholder="View" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="day">Day</SelectItem>
                      <SelectItem value="week">Week</SelectItem>
                      <SelectItem value="month">Month</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <CardTitle className="text-xl mt-2">
                  {format(date, "EEEE, MMMM d, yyyy")}
                </CardTitle>
                <CardDescription>
                  {todayEvents.length === 0 
                    ? "No events scheduled for today." 
                    : `${todayEvents.length} event${todayEvents.length > 1 ? 's' : ''} scheduled`}
                </CardDescription>
              </CardHeader>
              <CardContent>
                {todayEvents.length > 0 ? (
                  <div className="space-y-4">
                    {todayEvents.map(event => (
                      <div 
                        key={event.id} 
                        className="flex items-start gap-4 p-4 rounded-lg border border-muted hover:bg-muted/50 transition-colors"
                      >
                        <div className={`rounded-full p-2 ${
                          event.type === 'class' ? 'bg-blue-100 text-blue-600' : 
                          event.type === 'assignment' ? 'bg-amber-100 text-amber-600' : 
                          event.type === 'exam' ? 'bg-red-100 text-red-600' : 
                          'bg-gray-100 text-gray-600'
                        }`}>
                          {getEventIcon(event.type)}
                        </div>
                        
                        <div className="flex-1">
                          <div className="flex justify-between items-start">
                            <div>
                              <h3 className="font-medium">{event.title}</h3>
                              <p className="text-sm text-muted-foreground">{event.course}</p>
                            </div>
                            {getEventBadge(event.type)}
                          </div>
                          
                          {event.description && (
                            <p className="text-sm mt-1 text-gray-600">{event.description}</p>
                          )}
                          
                          {event.time && (
                            <p className="text-sm mt-2 font-medium">{event.time}</p>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-12">
                    <CalendarIcon className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
                    <h3 className="font-medium text-lg mb-1">No events for this day</h3>
                    <p className="text-muted-foreground">
                      Select a different day to view events or add a new event.
                    </p>
                    <Button variant="outline" className="mt-4">
                      Add Event
                    </Button>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </AppLayout>
  );
};

export default CalendarPage;
