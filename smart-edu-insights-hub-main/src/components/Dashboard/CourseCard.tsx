
import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { BookOpen } from "lucide-react";

interface CourseCardProps {
  title: string;
  instructor: string;
  progress: number;
  image?: string;
  dueAssignments?: number;
}

const CourseCard = ({ title, instructor, progress, image, dueAssignments = 0 }: CourseCardProps) => {
  return (
    <Card className="card-hover overflow-hidden">
      <div 
        className="h-24 bg-gradient-to-r from-lms-primary to-lms-secondary flex items-center justify-center"
        style={image ? { backgroundImage: `url(${image})`, backgroundSize: 'cover', backgroundPosition: 'center' } : {}}
      >
        {!image && <BookOpen className="h-10 w-10 text-white" />}
      </div>
      
      <CardContent className="p-4">
        <h3 className="font-semibold text-gray-800 mb-1">{title}</h3>
        <p className="text-sm text-gray-500 mb-3">{instructor}</p>
        
        <div className="flex items-center justify-between text-xs mb-1">
          <span>Progress</span>
          <span className="font-medium">{progress}%</span>
        </div>
        <Progress value={progress} className="h-1.5" />
        
        {dueAssignments > 0 && (
          <div className="mt-3 flex justify-between items-center">
            <span className="text-xs text-gray-500">Due assignments</span>
            <span className="bg-red-100 text-red-800 text-xs font-medium px-2 py-0.5 rounded">
              {dueAssignments}
            </span>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default CourseCard;
