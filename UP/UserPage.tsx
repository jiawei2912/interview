import axios from '@/lib/axios';
import { USER_QUERY_KEY } from '@/lib/constants';
import { getDownloadFileFunc } from '@/lib/utils';
import { useQuery } from '@tanstack/react-query';
import { ErrorPage } from '../common/ErrorPage';
import { FullPageLoading } from '../common/FullPageLoading';
import BaseTable from '../common/Table/BaseTable';
import { Button } from '../ui/button';
import {
  Dialog,
  DialogContent,
  DialogTitle,
  DialogTrigger,
} from '../ui/dialog';
import { CreateUserForm } from './CreateUserForm';
import { columns } from './columns';
import { User } from './types';

const UserPage = () => {
  const { isLoading, data, error, isError } = useQuery({
    queryKey: [USER_QUERY_KEY],
    queryFn: async () => {
      const params = {
        returnFormat: 'list',
      };
      const res = await axios.get<User[]>('/api/user/get_user/', { params });
      return res.data;
    },
  });

  // Query that downloads the table data as a file for the user
  const downloadFile = getDownloadFileFunc('users', '/api/user/get_user/', {
    returnFormat: 'file',
  });

  // Actions unique to this page
  const actionsRow = () => {
    return (
      <>
        <div className="flex items-center gap-4">
          <span className="mr-2">Actions:</span>
          <Dialog>
            <DialogTrigger asChild>
              <Button>Create User</Button>
            </DialogTrigger>
            <DialogContent className="overflow-y-auto md:max-w-5xl max-h-screen sm:max-w-wd">
              <DialogTitle>Create User Form</DialogTitle>
              <CreateUserForm />
            </DialogContent>
          </Dialog>
          {/* <EditUserSelfDialog /> */}
        </div>
      </>
    );
  };
  if (isLoading) return <FullPageLoading />;
  if (isError) {
    return <ErrorPage errorText={error?.toString()} />;
  }
  return (
    <>
      <BaseTable
        tableID="users_table"
        data={data!}
        columns={columns}
        downloadFile={downloadFile}
        actionsRow={actionsRow}
      />
    </>
  );
};

export default UserPage;
