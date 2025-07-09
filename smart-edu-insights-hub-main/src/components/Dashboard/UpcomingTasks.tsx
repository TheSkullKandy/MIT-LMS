
import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Calendar as CalendarIcon, ChevronRight, FileText, Video } from "lucide-react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";

interface Task {
  id: number;
  title: string;
  course: string;
  date: string;
  type: "assignment" | "class" | "exam";
}

const UpcomingTasks = () => {
  const [activeTab, setActiveTab] = useState<string>("all");
  
  const tasks: Task[] = [
    { id: 1, title: "Submit Project Proposal", course: "Advanced Programming", date: "Today, 11:59 PM", type: "assignment" },
    { id: 2, title: "Virtual Lecture", course: "Data Structures", date: "Tomorrow, 10:00 AM", type: "class" },
    { id: 3, title: "Mid-term Exam", course: "Algorithms", date: "May 20, 2:00 PM", type: "exam" },
    { id: 4, title: "Lab Report Submission", course: "Physics", date: "May 18, 11:59 PM", type: "assignment" },
    { id: 5, title: "Group Discussion", course: "Business Ethics", date: "May 19, 3:30 PM", type: "class" }
  ];
  
  const filteredTasks = activeTab === "all" 
    ? tasks 
    : tasks.filter(task => task.type === activeTab);
  
  const getTaskIcon = (type: string) => {
    switch(type) {
      case "assignment":
        return <FileText className="h-4 w-4" />;
      case "class":
        return <Video className="h-4 w-4" />;
      case "exam":
        return <FileText className="h-4 w-4" />;
      default:
        return <FileText className="h-4 w-4" />;
    }
  };
  
  return (
    <Card>
      <CardHeader className="pb-3">
        <CardTitle className="text-lg font-semibold">Upcoming Tasks</CardTitle>
      </CardHeader>
      <CardContent className="px-2">
        <Tabs defaultValue="all" value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="all">All</TabsTrigger>
            <TabsTrigger value="assignment">Assignments</TabsTrigger>
            <TabsTrigger value="class">Classes</TabsTrigger>
          </TabsList>
          
          <TabsContent value="all" className="mt-0">
            <TasksList tasks={filteredTasks} />
          </TabsContent>
          
          <TabsContent value="assignment" className="mt-0">
            <TasksList tasks={filteredTasks} />
          </TabsContent>
          
          <TabsContent value="class" className="mt-0">
            <TasksList tasks={filteredTasks} />
          </TabsContent>
        </Tabs>
        
        <div className="flex justify-center mt-3">
          <Button variant="ghost" size="sm" className="text-xs text-muted-foreground">
            View All
            <ChevronRight className="h-3 w-3 ml-1" />
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

interface TasksListProps {
  tasks: Task[];
}

const TasksList = ({ tasks }: TasksListProps) => {
  const getTaskIcon = (type: string) => {
    switch(type) {
      case "assignment":
        return <FileText className="h-4 w-4 text-lms-info" />;
      case "class":
        return <Video className="h-4 w-4 text-lms-success" />;
      case "exam":
        return <FileText className="h-4 w-4 text-lms-warning" />;
      default:
        return <FileText className="h-4 w-4" />;
    }
  };
  
  const getTaskTypeClass = (type: string) => {
    switch(type) {
      case "assignment":
        return "bg-blue-100 text-blue-800";
      case "class":
        return "bg-green-100 text-green-800";
      case "exam":
        return "bg-amber-100 text-amber-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };
  
  return (
    <div className="space-y-1">
      {tasks.length === 0 ? (
        <div className="text-center py-6">
          <p className="text-sm text-muted-foreground">No upcoming tasks</p>
        </div>
      ) : (
        tasks.map((task) => (
          <div
            key={task.id}
            className="flex items-center gap-3 p-3 rounded-md hover:bg-muted transition-colors cursor-pointer"
          >
            <div className="flex h-9 w-9 items-center justify-center rounded-md border">
              {getTaskIcon(task.type)}
            </div>
            <div className="flex-1 space-y-1">
              <div className="flex items-center justify-between">
                <p className="text-sm font-medium leading-none">{task.title}</p>
                <span className={`text-xs px-2 py-0.5 rounded-full ${getTaskTypeClass(task.type)}`}>
                  {task.type === "assignment" ? "Due" : task.type === "class" ? "Class" : "Exam"}
                </span>
              </div>
              <p className="text-xs text-muted-foreground">{task.course}</p>
            </div>
            
            <div className="flex items-center text-xs text-muted-foreground whitespace-nowrap">
              <CalendarIcon className="h-3 w-3 mr-1" />
              {task.date}
            </div>
          </div>
        ))
      )}
    </div>
  );
};

export default UpcomingTasks;
