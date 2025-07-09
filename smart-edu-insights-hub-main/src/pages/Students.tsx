
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Search, Filter, Download } from "lucide-react";
import AppLayout from "@/components/Layout/AppLayout";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

interface UserData {
  email: string;
  userType: string;
  name: string;
  isLoggedIn: boolean;
}

interface Student {
  id: number;
  name: string;
  email: string;
  grade: string;
  attendance: string;
  status: string;
  courses: number;
}

// Sample student data for demonstration
const sampleStudents: Student[] = [
  {
    id: 1,
    name: "Alice Johnson",
    email: "alice.johnson@university.edu",
    grade: "A",
    attendance: "98%",
    status: "active",
    courses: 4,
  },
  {
    id: 2,
    name: "Bob Smith",
    email: "bob.smith@university.edu",
    grade: "B+",
    attendance: "92%",
    status: "active",
    courses: 3,
  },
  {
    id: 3,
    name: "Charlie Brown",
    email: "charlie.brown@university.edu",
    grade: "A-",
    attendance: "95%",
    status: "active",
    courses: 4,
  },
  {
    id: 4,
    name: "Diana Prince",
    email: "diana.prince@university.edu",
    grade: "C",
    attendance: "85%",
    status: "warning",
    courses: 4,
  },
  {
    id: 5,
    name: "Eric Williams",
    email: "eric.williams@university.edu",
    grade: "B",
    attendance: "90%",
    status: "active",
    courses: 3,
  },
  {
    id: 6,
    name: "Fiona Garcia",
    email: "fiona.garcia@university.edu",
    grade: "A",
    attendance: "97%",
    status: "active",
    courses: 5,
  },
  {
    id: 7,
    name: "George Miller",
    email: "george.miller@university.edu",
    grade: "D+",
    attendance: "75%",
    status: "at-risk",
    courses: 4,
  },
  {
    id: 8,
    name: "Hannah Lee",
    email: "hannah.lee@university.edu",
    grade: "B-",
    attendance: "88%",
    status: "active",
    courses: 4,
  },
];

const Students = () => {
  const [userData, setUserData] = useState<UserData | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [students, setStudents] = useState<Student[]>(sampleStudents);
  const navigate = useNavigate();

  useEffect(() => {
    // Get user data from localStorage
    const userDataString = localStorage.getItem("lms-user");
    if (userDataString) {
      const parsedUserData = JSON.parse(userDataString);
      setUserData(parsedUserData);

      // If not faculty, redirect to dashboard
      if (parsedUserData.userType !== "faculty") {
        navigate("/dashboard");
      }
    } else {
      navigate("/");
    }
  }, [navigate]);

  // Filter students based on search query and status filter
  useEffect(() => {
    let filteredStudents = [...sampleStudents];
    
    if (searchQuery) {
      filteredStudents = filteredStudents.filter(
        student => 
          student.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
          student.email.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }
    
    if (statusFilter !== "all") {
      filteredStudents = filteredStudents.filter(
        student => student.status === statusFilter
      );
    }
    
    setStudents(filteredStudents);
  }, [searchQuery, statusFilter]);

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "active":
        return <Badge variant="outline" className="bg-green-500 text-white hover:bg-green-600">Active</Badge>;
      case "warning":
        return <Badge variant="outline" className="bg-amber-500 text-white hover:bg-amber-600">Warning</Badge>;
      case "at-risk":
        return <Badge variant="outline" className="bg-red-500 text-white hover:bg-red-600">At Risk</Badge>;
      default:
        return <Badge>{status}</Badge>;
    }
  };

  if (!userData) {
    return <div>Loading...</div>;
  }

  return (
    <AppLayout>
      <div className="max-w-7xl mx-auto">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-800">Student Management</h1>
          <p className="text-gray-600">
            Monitor and manage your students' performance and progress.
          </p>
        </div>

        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6">
          <div className="relative w-full md:w-96">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-gray-500" />
            <Input
              type="search"
              placeholder="Search students..."
              className="pl-8"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>

          <div className="flex flex-col sm:flex-row gap-3 w-full md:w-auto">
            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger className="w-full sm:w-40">
                <SelectValue placeholder="Filter by status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Statuses</SelectItem>
                <SelectItem value="active">Active</SelectItem>
                <SelectItem value="warning">Warning</SelectItem>
                <SelectItem value="at-risk">At Risk</SelectItem>
              </SelectContent>
            </Select>

            <Button variant="outline" className="flex gap-2">
              <Download className="h-4 w-4" />
              <span>Export</span>
            </Button>
          </div>
        </div>

        <Card>
          <div className="rounded-md border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Student</TableHead>
                  <TableHead>Email</TableHead>
                  <TableHead>Avg. Grade</TableHead>
                  <TableHead>Attendance</TableHead>
                  <TableHead>Courses</TableHead>
                  <TableHead>Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {students.length > 0 ? (
                  students.map((student) => (
                    <TableRow key={student.id}>
                      <TableCell className="font-medium flex items-center gap-3">
                        <Avatar className="h-8 w-8">
                          <AvatarFallback>{student.name[0]}</AvatarFallback>
                        </Avatar>
                        {student.name}
                      </TableCell>
                      <TableCell>{student.email}</TableCell>
                      <TableCell>{student.grade}</TableCell>
                      <TableCell>{student.attendance}</TableCell>
                      <TableCell>{student.courses}</TableCell>
                      <TableCell>{getStatusBadge(student.status)}</TableCell>
                    </TableRow>
                  ))
                ) : (
                  <TableRow>
                    <TableCell colSpan={6} className="text-center py-8 text-gray-500">
                      No students found matching your criteria.
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </div>
        </Card>
      </div>
    </AppLayout>
  );
};

export default Students;
