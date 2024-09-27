"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import React, { Dispatch, SetStateAction } from "react";
import { useForm } from "react-hook-form";
import * as z from "zod";

import { deleteProvider } from "@/actions";
import { DeleteIcon } from "@/components/icons";
import { useToast } from "@/components/ui";
import { CustomButton } from "@/components/ui/custom";
import { Form } from "@/components/ui/form";

const formSchema = z.object({
  providerId: z.string(),
});

export const DeleteForm = ({
  providerId,
  setIsOpen,
}: {
  providerId: string;
  setIsOpen: Dispatch<SetStateAction<boolean>>;
}) => {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
  });
  const { toast } = useToast();
  const isLoading = form.formState.isSubmitting;

  async function onSubmitClient(formData: FormData) {
    // client-side validation
    const data = await deleteProvider(formData);

    if (data?.errors && data.errors.length > 0) {
      const error = data.errors[0];
      const errorMessage = `${error.detail}`;
      // show error
      toast({
        variant: "destructive",
        title: "Oops! Something went wrong",
        description: errorMessage,
      });
    } else {
      toast({
        title: "Success!",
        description: "The provider was removed successfully.",
      });
    }
    setIsOpen(false); // Close the modal on success
  }

  return (
    <Form {...form}>
      <form action={onSubmitClient}>
        <input type="hidden" name="id" value={providerId} />
        <div className="w-full flex justify-center sm:space-x-6">
          <CustomButton
            type="button"
            className="w-full bg-transparent"
            variant="faded"
            size="lg"
            radius="lg"
            onPress={() => setIsOpen(false)}
            disabled={isLoading}
          >
            <span>Cancel</span>
          </CustomButton>

          <CustomButton
            type="submit"
            className="w-full"
            variant="solid"
            color="danger"
            size="lg"
            isLoading={isLoading}
            startContent={!isLoading && <DeleteIcon size={24} />}
          >
            {isLoading ? <>Loading</> : <span>Delete</span>}
          </CustomButton>
        </div>
      </form>
    </Form>
  );
};
